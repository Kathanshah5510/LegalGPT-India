import pickle

with open(
    r"D:\MTech\Projects\LegalGPT-India\vector_db\chunks.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

for i, chunk in enumerate(chunks):

    if "No person shall be deprived of his life" in chunk:

        print("=" * 50)
        print("FOUND")
        print("Chunk Index:", i)
        print("=" * 50)

        print(chunk)

        break