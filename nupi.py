# Import Libraries

import streamlit as st
import matplotlib.pyplot as plt
import base64
import io
import numpy as np

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


# Page Config

st.set_page_config(
    page_title="Smart DNA Quality Analyzer",
    page_icon="🧬",
    layout="wide"
)


# Background Function

def set_bg(image):

    with open(image, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Tabs

tabs = st.tabs([
"🏠 Home",
"🧪 Tool",
"📖 About",
"⚙ Working",
"📊 Applications",
"🚀 Future Scope",
"👥 Team"
])


# Home

with tabs[0]:

    set_bg("background.jpg")

    st.title("🧬 Smart DNA Quality Analyzer")

    st.markdown("""
Bioinformatics DNA Quality Control Platform

Adapter Sequence Removal  
GC Content Analysis  
Quality Score Analysis  
Sequence Length Distribution  
Duplicate Sequence Detection  
Nucleotide Frequency Analysis  
Variant Calling  
Read Statistics  
Quality Control Graphs  
PDF Report Generation
""")


# Tool

with tabs[1]:

    set_bg("background.jpg")

    st.title("DNA Quality Analysis Tool")

    uploaded_file = st.file_uploader(
    "Upload FASTQ File",
    type=["fastq","fq"]
    )

    run = st.button("Run Analysis")


# Adapter Removal

    def remove_adapter(seq):
        return seq.replace("AGATCGGAAGAGC","")


# Variant Calling

    def variant_calling(seqs):

        reference = seqs[0]
        variants = []

        for seq in seqs:
            for i in range(min(len(seq),len(reference))):
                if seq[i]!=reference[i]:
                    variants.append(
                    f"Position {i+1}: {reference[i]} → {seq[i]}"
                    )

        return variants


# Processing

    if run and uploaded_file:

        lines=uploaded_file.read().decode(
        errors="ignore").splitlines()

        sequences=[]
        qualities=[]

        max_reads=10000

        for i in range(0,min(len(lines),max_reads*4),4):

            if i+3<len(lines):

                sequences.append(lines[i+1])
                qualities.append(lines[i+3])


        cleaned=[remove_adapter(s) for s in sequences]


# Adapter Removal

        st.subheader("Adapter Removal")

        adapter_removed=sum(
        [1 for s in sequences if "AGATCGGAAGAGC" in s])

        st.write("Adapter Removed Reads:",adapter_removed)


# Read Statistics

        st.subheader("Read Statistics")

        read_count=len(cleaned)

        lengths=[len(s) for s in cleaned]

        st.write("Total Reads:",read_count)
        st.write("Minimum Length:",min(lengths))
        st.write("Maximum Length:",max(lengths))
        st.write("Average Length:",round(np.mean(lengths),2))


# GC Content

        st.subheader("GC Content Analysis")

        gc=[((s.count("G")+s.count("C"))/len(s))*100
        for s in cleaned]

        avg_gc=np.mean(gc)

        st.write("Average GC Content:",
        round(avg_gc,2))


# Quality Score

        st.subheader("Quality Score Analysis")

        scores=[]

        for q in qualities:
            scores.extend([ord(c)-33 for c in q])

        avg_quality=np.mean(scores)

        st.write("Average Quality Score:",
        round(avg_quality,2))

        plt.figure(figsize=(5,3))
        plt.plot(scores,color="blue")
        plt.title("Quality Score Distribution")
        plt.savefig("quality.png")
        st.pyplot(plt)


# Nucleotide Frequency

        st.subheader("Nucleotide Frequency")

        A=T=G=C=0

        for s in cleaned:
            A+=s.count("A")
            T+=s.count("T")
            G+=s.count("G")
            C+=s.count("C")

        plt.figure(figsize=(5,3))

        plt.bar(
        ["A","T","G","C"],
        [A,T,G,C],
        color=["#4CAF50","#2196F3","#FF9800","#E91E63"]
        )

        plt.title("Nucleotide Frequency")
        plt.savefig("nucleotide.png")
        st.pyplot(plt)


# Variant Calling

        st.subheader("Variant Calling")

        variants=variant_calling(cleaned)

        st.write("Total Variants:",len(variants))

        for v in variants[:20]:
            st.write(v)


# PDF (UPDATED ONLY THIS PART)

        def generate_pdf():

            styles=getSampleStyleSheet()
            story=[]

            story.append(
            Paragraph("Smart DNA Quality Analyzer Report",
            styles['Heading1'])
            )

            story.append(Spacer(1,10))

            story.append(Paragraph("Adapter Removal",styles['Heading2']))
            story.append(Paragraph(f"Adapter Removed Reads: {adapter_removed}",styles['Normal']))
            story.append(Spacer(1,10))

            story.append(Paragraph("Read Statistics",styles['Heading2']))
            story.append(Paragraph(f"Total Reads: {read_count}",styles['Normal']))
            story.append(Paragraph(f"Minimum Length: {min(lengths)}",styles['Normal']))
            story.append(Paragraph(f"Maximum Length: {max(lengths)}",styles['Normal']))
            story.append(Paragraph(f"Average Length: {round(np.mean(lengths),2)}",styles['Normal']))
            story.append(Spacer(1,10))

            story.append(Paragraph("GC Content Analysis",styles['Heading2']))
            story.append(Paragraph(f"Average GC Content: {round(avg_gc,2)}%",styles['Normal']))
            story.append(Spacer(1,10))

            story.append(Paragraph("Quality Score Analysis",styles['Heading2']))
            story.append(Paragraph(f"Average Quality Score: {round(avg_quality,2)}",styles['Normal']))
            story.append(Spacer(1,10))

            story.append(Paragraph("Quality Score Graph",styles['Heading2']))
            story.append(Image("quality.png",350,180))
            story.append(Spacer(1,10))

            story.append(Paragraph("Nucleotide Frequency Graph",styles['Heading2']))
            story.append(Image("nucleotide.png",350,180))
            story.append(Spacer(1,10))

            story.append(Paragraph("Variant Calling",styles['Heading2']))
            story.append(Paragraph(f"Total Variants: {len(variants)}",styles['Normal']))

            for v in variants[:20]:
                story.append(Paragraph(v,styles['Normal']))

            buffer=io.BytesIO()
            doc=SimpleDocTemplate(buffer,pagesize=A4)
            doc.build(story)

            pdf=buffer.getvalue()
            buffer.close()

            return pdf


        pdf=generate_pdf()

        st.download_button(
        "Download Full PDF Report",
        data=pdf,
        file_name="DNA_Report.pdf"
        )


# About

with tabs[2]:

    set_bg("background.jpg")

    st.title("About")

    st.write("""
DNA sequencing quality analysis  
FASTQ file processing  
Adapter sequence removal  
Variant detection  
Graph visualization  
Report generation
""")


# Working

with tabs[3]:

    set_bg("background.jpg")

    st.title("Working")

    st.write("""
Upload FASTQ file  
Run analysis  
Adapter removal  
Quality score calculation  
Variant detection  
Download report
""")


# Applications

with tabs[4]:

    set_bg("background.jpg")

    st.title("Applications")

    st.write("""
Genomics research  
Mutation detection  
Clinical genomics  
DNA quality control  
NGS data analysis  
Bioinformatics learning
""")


# Future Scope

with tabs[5]:

    set_bg("background.jpg")

    st.title("Future Scope")

    st.write("""
Machine learning integration  
Cloud deployment  
Large dataset analysis  
Real time sequencing  
Multi omics integration  
Genome annotation
""")


# Team

with tabs[6]:

    set_bg("background.jpg")

    st.title("Project Team Members")

    st.subheader("Nupur Nisal")
    st.write("Bioinformatics Developer")
    st.write("3522511009@gmail.com")
    st.markdown(
    "[LinkedIn](https://www.linkedin.com/in/nupur-nisal-543b46313)"
    )

    st.markdown("---")

    st.subheader("Vinita Salvi")
    st.write("Bioinformatics Analyst")
    st.write("3522511010@gmail.com")
    st.markdown(
    "[LinkedIn](https://www.linkedin.com/in/vinita-salvi27)"
    )