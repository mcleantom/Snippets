"""
A more efficient method of regular grid interpolation than scipy. Works especially well for higher dimension
interpolation
"""

class Intergrid:
    __doc__ = globals()["__doc__"]

    def __init__(self, griddata, lo, hi, maps=[], copy=True, verbose=1,
                 order=1, prefilter=False, fill_value=np.nan):
        self.fill_value = fill_value
        griddata = np.asanyarray(griddata)
        dim = griddata.ndim  # - (griddata.shape[-1] == 1)  # ??
        assert dim >= 2, griddata.shape
        self.dim = dim
        if np.isscalar(lo):
            lo *= np.ones(dim)
        if np.isscalar(hi):
            hi *= np.ones(dim)
        self.loclip = lo = np.asarray_chkfinite(lo).copy()
        self.hiclip = hi = np.asarray_chkfinite(hi).copy()
        assert lo.shape == (dim,), lo.shape
        assert hi.shape == (dim,), hi.shape
        self.copy = copy
        self.verbose = verbose
        self.order = order
        if order > 1 and 0 < prefilter < 1:  # 1/3: Mitchell-Netravali = 1/3 B + 2/3 fit
            exactfit = spline_filter(griddata)  # see Unser
            griddata += prefilter * (exactfit - griddata)
            prefilter = False
        self.griddata = griddata
        self.prefilter = (prefilter == True)

        self.maps = maps
        self.nmap = 0
        if len(maps) > 0:
            assert len(maps) == dim, "maps must have len %d, not %d" % (
                dim, len(maps))
            # linear maps (map None): Xcol -= lo *= scale -> [0, n-1]
            # nonlinear: np.interp e.g. [50 52 62 63] -> [0 1 2 3]
            self._lo = np.zeros(dim)
            self._scale = np.ones(dim)

            for j, (map, n, l, h) in enumerate(zip(maps, griddata.shape, lo, hi)):
                ## print "test: j map n l h:", j, map, n, l, h
                if map is None or callable(map):
                    self._lo[j] = l
                    if h > l:
                        self._scale[j] = (n - 1) / (h - l)  # _map lo -> 0, hi -> n - 1
                    else:
                        self._scale[j] = 0  # h <= l: X[:,j] -> 0
                    continue
                self.maps[j] = map = np.asanyarray(map)
                self.nmap += 1
                assert len(map) == n, "maps[%d] must have len %d, not %d" % (
                    j, n, len(map))
                mlo, mhi = map.min(), map.max()
                if not (l <= mlo <= mhi <= h):
                    print("Warning: Intergrid maps[%d] min %.3g max %.3g " \
                          "are outside lo %.3g hi %.3g" % (
                              j, mlo, mhi, l, h))

    # ...............................................................................
    def _map_to_uniform_grid(self, X):
        """ clip, map X linear / nonlinear  inplace """
        np.clip(X, self.loclip, self.hiclip, out=X)
        # X nonlinear maps inplace --
        for j, map in enumerate(self.maps):
            if map is None:
                continue
            if callable(map):
                X[:, j] = map(X[:, j])  # clip again ?
            else:
                # PWL e.g. [50 52 62 63] -> [0 1 2 3] --
                X[:, j] = np.interp(X[:, j], map, np.arange(len(map)))

            # linear map the rest, inplace (nonlinear _lo 0, _scale 1: noop)
        if self.nmap < self.dim:
            X -= self._lo
            X *= self._scale  # (griddata.shape - 1) / (hi - lo)
        ## print "test: _map_to_uniform_grid", X.T

    # ...............................................................................
    def __call__(self, X, out=None):
        """ query_values = Intergrid(...) ( query_points npt x dim )
        """
        X = np.asanyarray(X)
        assert X.shape[-1] == self.dim, ("the query array must have %d columns, "
                                         "but its shape is %s" % (self.dim, X.shape))

        if self.fill_value is not None:
            out_of_bounds = np.where(~ ((self.loclip <= X) & (X <= self.hiclip)).all(axis=1))

        Xdim = X.ndim
        if Xdim == 1:
            X = np.asarray([X])  # in a single point -> out scalar
        if self.copy:
            X = X.copy()
        assert X.ndim == 2, X.shape
        npt = X.shape[0]
        if out is None:
            out = np.empty(npt, dtype=self.griddata.dtype)
        t0 = time()
        self._map_to_uniform_grid(X)  # X inplace
        # ...............................................................................
        map_coordinates(self.griddata, X.T,
                        order=self.order, prefilter=self.prefilter,
                        mode="nearest",  # outside -> edge
                        # test: mode="constant", cval=np.NaN,
                        output=out)
        if self.verbose:
            print("Intergrid: %.3g msec  %d points in a %s grid  %d maps  order %d" % (
                (time() - t0) * 1000, npt, self.griddata.shape, self.nmap, self.order))

        if self.fill_value is not None:
            out[out_of_bounds] = self.fill_value

        return out if Xdim == 2 else out[0]

    at = __call__