from dataset_loader import DatasetLoader


loader = DatasetLoader()

df = loader.load_dataset()

print("=" * 60)
print("Dataset Information")
print("=" * 60)

print()

print(df.info())

print()

print("=" * 60)

print(df.describe(include="all"))

print()

print("=" * 60)

print("Shape :", df.shape)

print()

print("Columns")

print(df.columns)

print()

print("Missing Values")

print(df.isnull().sum())

print()

print("Duplicate Rows")

print(df.duplicated().sum())