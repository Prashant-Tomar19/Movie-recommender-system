import pickle, gzip

with open("similarity.pkl", "rb") as f_in:
    with gzip.open("similarity.pkl.gz", "wb") as f_out:
        f_out.writelines(f_in)
