from bayesian_network import SimpleBN


def pretty_print_probs(probs):
    for s, p in probs.items():
        print(f"  {s}: {p:.3f}")


def discretize_record(raw):
    # map raw fields into BN states
    m = {}
    h = raw.get("Humidity")
    if isinstance(h, (int, float)):
        if h < 40:
            m["Humidity"] = "Low"
        elif h < 70:
            m["Humidity"] = "Medium"
        else:
            m["Humidity"] = "High"
    else:
        if h is not None:
            m["Humidity"] = str(h).title()

    nd = raw.get("NDVI")
    try:
        v = float(nd)
        if v < 0.3:
            m["NDVI"] = "Poor"
        elif v < 0.6:
            m["NDVI"] = "Moderate"
        else:
            m["NDVI"] = "Good"
    except Exception:
        if nd is not None:
            m["NDVI"] = str(nd).title()

    ft = raw.get("fertilizer_type") or raw.get("FertilizerType")
    if ft is not None:
        s = str(ft).strip().lower()
        if "none" in s or s == "":
            m["FertilizerType"] = "None"
        elif "organ" in s:
            m["FertilizerType"] = "Organic"
        elif "inorg" in s or "mix" in s or "mixed" in s:
            # treat Inorganic and Mixed as non-organic (map to Synthetic)
            m["FertilizerType"] = "Synthetic"
        else:
            m["FertilizerType"] = "Synthetic"

    pu = raw.get("pesticide_usage_ml") or raw.get("pesticide_usage")
    try:
        pv = float(pu)
        if pv < 50:
            m["PesticideUsage"] = "Low"
        elif pv < 150:
            m["PesticideUsage"] = "Medium"
        else:
            m["PesticideUsage"] = "High"
    except Exception:
        if pu is not None:
            m["PesticideUsage"] = str(pu).title()

    y = raw.get("yield_kg_per_hectare") or raw.get("yield")
    try:
        yv = float(y)
        if yv < 2000:
            m["Yield"] = "Low"
        elif yv < 4000:
            m["Yield"] = "Medium"
        else:
            m["Yield"] = "High"
    except Exception:
        pass

    cd = raw.get("crop_disease_status") or raw.get("CropDiseaseStatus")
    if cd is not None:
        s = str(cd).strip().lower()
        if "sev" in s or "severe" in s:
            m["CropDiseaseStatus"] = "Severe"
        elif "mod" in s or "mild" in s or "min" in s or "minor" in s:
            # map both Mild and Moderate to 'Minor' state in CPT
            m["CropDiseaseStatus"] = "Minor"
        elif "none" in s or s == "":
            m["CropDiseaseStatus"] = "None"
        else:
            m["CropDiseaseStatus"] = "Minor"

    return m


def main():
    bn = SimpleBN()

    record = {
        "Humidity": 78,
        "fertilizer_type": "Organic",
        "pesticide_usage_ml": 30,
        "yield_kg_per_hectare": 1800,
        "NDVI": 0.45,
        "crop_disease_status": "Minor",
    }

    print("Record:")
    for k, v in record.items():
        print(f" - {k}: {v}")

    evidence = discretize_record(record)
    print("\nEvidence for BN:")
    for k, v in evidence.items():
        print(f" - {k}: {v}")

    posterior = bn.infer_pest_posterior(evidence)
    print("\nPosterior:")
    pretty_print_probs(posterior)

    risk, p = bn.classify_risk(posterior)
    print(f"\nRisk: {risk} (prob {p:.3f})")

    print("\nNotes:")
    print(" - Low pesticide and low yield raise risk.")
    print(" - High humidity and moderate NDVI give mixed signals.")

    print("\nD-sep examples:")
    print(" Humidity and PesticideUsage independent given PestOutbreak? ->", bn.is_d_separated("Humidity", "PesticideUsage", ["PestOutbreak"]))


if __name__ == '__main__':
    main()
