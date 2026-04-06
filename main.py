from data_generator import DataGenerator


def main() -> None:
    generator = DataGenerator()
    my_data = generator.financial.generate()
    print(my_data)


if __name__ == "__main__":
    main()
