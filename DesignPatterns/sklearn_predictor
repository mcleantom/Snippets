from sklearn.base import BaseEstimator, RegressorMixin
from pydantic import BaseModel


class EmpericalFormulaParameters(BaseModel):
    length: float
    width: float


class EmpericalPredictor(BaseEstimator, RegressorMixin):
   """
   Example usage:
       emperical_predictor = EmpericalPredictor(EmpericalFormulaParameters(length=10, width=5))
       heights = np.arange(1, 10)
       volumes = emperical_predictor.predict(heights)
   """

    def __init__(self, emperical_formula_parameters: EmpericalFormulaParameters):
        self.emperical_formula_parameters = emperical_parameters
        
    def fit(self):
        return self
    
    def predict(self, X):
        return np.apply_along_axis(self._predict, axis=1, arr=X)
        
    def _predict(self, X):
        return self.emperical_formula_parameters.length * self.emperical_formula_parameters.width * X
