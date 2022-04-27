class Factory:
    factory_handlers = {}

    @classmethod
    def factory(cls, handle_id):
        try:
            handler = cls.factory_handlers[handle_id]
        except KeyError as err:
            raise NotImplementedError(f"{handle_id} does not exist in the factory")
        return handler

    @classmethod
    def register(cls, handle_id):
        def deco(deco_cls):
            cls.factory_handlers[handle_id] = deco_cls
            return deco_cls
        return deco

# EXAMPLE
if __name__ == "__main__":
    import os

    class ReadManager(Factory):
        @classmethod
        def read(cls, file):
            name, extension = os.path.splitext(f.name)
            extension = extension.lstrip('.')
            read_func = cls.factory(extension)
            read_func(file)

    @ReadManager.register("csv")
    def read_csv(file):
        print(f"Reading file as CSV")

    @ReadManager.register("pdf")
    def read_pdf(file):
        print(f"Reading file as PDF")
    
    @ReadManager.register("txt")
    def read_txt(file):
        print(f"Reading file as txt")

    with open("test_file.txt", "r") as f:
        ReadManager.read(f)

    with open("test.jpg", "r") as f:
        ReadManager.read(f)
