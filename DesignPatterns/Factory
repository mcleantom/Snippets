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
    class SaveManager(Factory):

        def save(self, type, file):
            save_func = self.factory(type)
            save_func(file)


    @SaveManager.register("csv")
    def save_csv(file):
        print(f"Saving {file} as CSV")


    @SaveManager.register("pdf")
    def save_pdf(file):
        print(f"Saving {file} as PDF")

    save_manager = SaveManager()
    file = "hello"
    save_manager.save("csv", file)
    save_manager.save("pdf", file)
