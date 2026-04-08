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
    page_title="Smart DNA Quality Analyzer 1.3",
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

    st.title("🧬 Smart DNA Quality Analyzer 1.3")

    st.markdown("""
### Bioinformatics DNA Quality Control Platform

Smart DNA Quality Analyzer is developed for DNA sequencing 
quality control and FASTQ data analysis.

Features

Adapter Sequence Removal  
GC Content Analysis  
Quality Score Analysis  
Sequence Length Distribution  
Duplicate Sequence Detection  
Nucleotide Frequency Analysis  
Variant Calling  
Read Statistics  
Quality Control Graphs  
FASTQ File Support  
PDF Report Generation  
""")


# Tool Section

with tabs[1]:

    set_bg("background.jpg")

    st.title("DNA Quality Analysis Tool")

    option = st.radio(
    "Select Input",
    ["Upload FASTQ File","Use Demo Data"]
    )

    uploaded_file=None

    if option=="Upload FASTQ File":
        uploaded_file=st.file_uploader(
        "Upload FASTQ File",
        type=["fastq","fq"]
        )


    demo_fastq="""@SEQ_1
ATGCGTACGTAGCTAGATCGGAAGAGC
+
IIIIIIIIIIIIIIIIIIIIIIIIIII
@SEQ_2
ATGCGTACGTAGCTAGATCGGAAGAGC
+
IIIIIIIIIIIIIIIIIIIIIIIIIII
"""


# Adapter Removal

    def remove_adapter(seq):
        return seq.replace("AGATCGGAAGAGC","")


# Variant Calling

    def variant_calling(seqs):

        reference=seqs[0]
        variants=[]

        for seq in seqs:

            for i in range(min(len(seq),len(reference))):

                if seq[i]!=reference[i]:

                    variants.append(
                    f"Position {i+1}: {reference[i]} → {seq[i]}"
                    )

        return variants


# Processing

    if uploaded_file or option=="Use Demo Data":

        if option=="Use Demo Data":
            lines=demo_fastq.split("\n")
        else:
            lines=uploaded_file.read().decode().split("\n")

        sequences=[]
        qualities=[]

        for i in range(0,len(lines),4):

            if i+3<len(lines):

                sequences.append(lines[i+1])
                qualities.append(lines[i+3])

        cleaned=[remove_adapter(s) for s in sequences]


# Adapter Removal

        st.subheader("Adapter Removal")

        adapter_removed=sum([1 for s in sequences if "AGATCGGAAGAGC" in s])

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

        gc=[((s.count("G")+s.count("C"))/len(s))*100 for s in cleaned]
        avg_gc=np.mean(gc)

        st.write("Average GC Content:",round(avg_gc,2))


# Quality Score

        st.subheader("Quality Score Analysis")

        scores=[]

        for q in qualities:
            scores.extend([ord(c)-33 for c in q])

        avg_quality=np.mean(scores)

        st.write("Average Quality Score:",round(avg_quality,2))

        plt.figure(figsize=(4,2.5))
        plt.plot(scores,color="green")
        plt.title("Quality Score")
        plt.tight_layout()
        plt.savefig("quality.png")
        st.pyplot(plt)


# Sequence Length

        st.subheader("Sequence Length Distribution")

        plt.figure(figsize=(4,2.5))
        plt.hist(lengths,color="orange")
        plt.title("Sequence Length")
        plt.tight_layout()
        plt.savefig("length.png")
        st.pyplot(plt)


# Duplicate Detection

        st.subheader("Duplicate Detection")

        duplicates=len(cleaned)-len(set(cleaned))

        st.write("Duplicate Reads:",duplicates)


# Nucleotide Frequency

        st.subheader("Nucleotide Frequency")

        A=T=G=C=0

        for s in cleaned:
            A+=s.count("A")
            T+=s.count("T")
            G+=s.count("G")
            C+=s.count("C")

        plt.figure(figsize=(4,2.5))
        plt.bar(["A","T","G","C"],
        [A,T,G,C],
        color=["blue","red","green","purple"])

        plt.title("Nucleotide Frequency")
        plt.tight_layout()
        plt.savefig("nucleotide.png")
        st.pyplot(plt)


# Variant Calling

        st.subheader("Variant Calling")

        variants=variant_calling(cleaned)

        st.write("Total Variants:",len(variants))

        for v in variants[:20]:
            st.write(v)


# PDF Report

        def generate_pdf():

            styles=getSampleStyleSheet()
            story=[]

            story.append(
            Paragraph("Smart DNA Quality Analyzer 1.3 Report",
            styles['Heading1'])
            )

            story.append(Spacer(1,12))

            story.append(Paragraph(
            f"Adapter Removed Reads: {adapter_removed}",
            styles['Normal']))

            story.append(Paragraph(
            f"Total Reads: {read_count}",
            styles['Normal']))

            story.append(Paragraph(
            f"Minimum Length: {min(lengths)}",
            styles['Normal']))

            story.append(Paragraph(
            f"Maximum Length: {max(lengths)}",
            styles['Normal']))

            story.append(Paragraph(
            f"Average Length: {round(np.mean(lengths),2)}",
            styles['Normal']))

            story.append(Paragraph(
            f"Average GC Content: {round(avg_gc,2)}",
            styles['Normal']))

            story.append(Paragraph(
            f"Average Quality Score: {round(avg_quality,2)}",
            styles['Normal']))

            story.append(Spacer(1,20))

            story.append(Image("quality.png",350,180))
            story.append(Spacer(1,15))

            story.append(Image("length.png",350,180))
            story.append(Spacer(1,15))

            story.append(Image("nucleotide.png",350,180))

            story.append(PageBreak())

            story.append(Paragraph(
            f"Duplicate Reads: {duplicates}",
            styles['Normal']))

            story.append(Spacer(1,15))

            story.append(Paragraph("Variant Calling",
            styles['Heading2']))

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
        "Download Full Report PDF",
        data=pdf,
        file_name="Smart_DNA_Report.pdf",
        mime="application/pdf"
        )


# About

with tabs[2]:

    set_bg("background.jpg")

    st.title("About")

    st.write("""
Smart DNA Quality Analyzer is developed for DNA sequencing quality analysis.

• FASTQ file quality analysis  
• Adapter removal  
• GC content calculation  
• Variant detection  
• Graph visualization  
• Report generation  
""")


# Working

with tabs[3]:

    set_bg("background.jpg")

    st.title("Working")

    st.write("""
• Upload FASTQ file  
• Extract sequences  
• Remove adapters  
• Perform analysis  
• Detect variants  
• Generate report  
""")


# Applications

with tabs[4]:

    set_bg("background.jpg")

    st.title("Applications")

    st.write("""
• DNA quality control  
• Genomics research  
• Mutation detection  
• Clinical genomics  
• Microbial genomics  
• Bioinformatics learning  
""")


# Future Scope

with tabs[5]:

    set_bg("background.jpg")

    st.title("Future Scope")

    st.write("""
• Machine learning integration  
• Large scale NGS analysis  
• Cloud deployment  
• Multi sample comparison  
• Advanced variant detection  
• Real time sequencing  
""")


# Team

with tabs[6]:

    set_bg("background.jpg")

    st.title("Project Team Members")

    st.subheader("Nupur Nisal")
    st.write("Bioinformatics Developer")
    st.write("3522511009@gmail.com")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/nupur-nisal-543b46313)")

    st.markdown("---")

    st.subheader("Vinita Salvi")
    st.write("Bioinformatics Analyst")
    st.write("3522511010@gmail.com")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/vinita-salvi27)")