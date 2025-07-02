"""
Downloads real public compliance documents for POC.
Sources: SEC, OFAC, FATF, FinCEN, EU Annex sanctions.
"""

import requests
from pathlib import Path

# Pasta onde os arquivos serão salvos
data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)

# Cabeçalho para evitar bloqueios (403)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Lista de arquivos a baixar
files = [
    # SEC filings (formato .txt)
    {
        "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108.txt",
        "filename": "apple_10k_2022.txt"
    },
    {
        "url": "https://www.sec.gov/Archives/edgar/data/789019/000156459022026876/0001564590-22-026876.txt",
        "filename": "microsoft_10k_2022.txt"
    },

    # Lista de sanções OFAC (formato .csv)
    {
        "url": "https://www.treasury.gov/ofac/downloads/sdn.csv",
        "filename": "ofac_sdn_list.csv"
    },

    # PDF com recomendações oficiais do FATF
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/recommendations/FATF%20Recommendations%202012.pdf",
        "filename": "fatf_recommendations.pdf"
    },

    # PDF com alerta do FinCEN (lavagem de dinheiro e ransomware)
    {
        "url": "https://www.fincen.gov/sites/default/files/advisory/2021-11-08/FinCEN%20Ransomware%20Advisory_FINAL_508_.pdf",
        "filename": "fincen_ransomware_advisory.pdf"
    },

    # PDF com anexo oficial de sanções da União Europeia
    {
        "url": "https://www.eeas.europa.eu/sites/default/files/documents/annex_2_sanctions_related_commitments_en_0.pdf",
        "filename": "eu_annex2_sanctions.pdf"
    },
    
        # Additional FinCEN & FATF PDFs
    {
        "url": "https://www.fincen.gov/sites/default/files/advisory/2022-04-14/FinCEN%20Advisory%20Corruption%20FINAL%20508.pdf",
        "filename": "fincen_advisory_corruption_2022.pdf"
    },
    {
        "url": "https://www.fincen.gov/sites/default/files/advisory/2022-06-15/FinCEN%20Advisory%20Elder%20Financial%20Exploitation%20FINAL%20508.pdf",
        "filename": "fincen_advisory_elder_exploitation_2022.pdf"
    },
    {
        "url": "https://www.fincen.gov/sites/default/files/shared/FinCEN_Alert_Pig_Butchering_FINAL_508c.pdf",
        "filename": "fincen_alert_pig_butchering_2023.pdf"
    },
    {
        "url": "https://www.fincen.gov/sites/default/files/2022-03/FinCEN%20Alert%20Russian%20Elites%20High%20Value%20Assets_508%20FINAL.pdf",
        "filename": "fincen_alert_russian_elites_2022.pdf"
    },
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/publications/FATF-Annual-Report-2022-2023.pdf.coredownload.pdf",
        "filename": "fatf_annual_report_2022-2023.pdf"
    },
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/methodology/FATF-Assessment-Methodology-2022.pdf.coredownload.inline.pdf",
        "filename": "fatf_assessment_methodology_2022.pdf"
    },
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/reports/Report-on-the-State-of-Effectiveness-Compliance-with-FATF-Standards.pdf.coredownload.pdf",
        "filename": "fatf_effectiveness_compliance_report_2022.pdf"
    },
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/methodology/Assessment-Follow-Up-ICRG-Procedures-2022.pdf.coredownload.inline.pdf",
        "filename": "fatf_procedures_mutual_evaluations_2022.pdf"
    },
    {
        "url": "https://www.fatf-gafi.org/content/dam/fatf-gafi/publications/FATF-Universal-Procedures.pdf.coredownload.inline.pdf",
        "filename": "fatf_universal_procedures.pdf"
    }
    
]

# Função para baixar
def download(url, filename):
    path = data_dir / filename
    if path.exists():
        print(f" === Already downloaded: {filename} ===")
        return

    print(f"=== Downloading: {filename}===")
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        path.write_bytes(response.content)
        print(f"=== Downloaded: {filename}===")
    else:
        print(f"=== Failed: {filename} ({response.status_code})===")

# Execução
if __name__ == "__main__":
    for file in files:
        download(file["url"], file["filename"])
