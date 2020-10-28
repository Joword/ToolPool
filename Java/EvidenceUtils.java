package com.bgi.interpretation.modules.sys.utils;

/**
 * @author WJT
 * @date 2020/2/22
 */
public class EvidenceUtils {

    public static String getPVS1Dec(String PVS1Dec){
        String Dec = PVS1Dec;
        if ("NA".equals(PVS1Dec)||null==PVS1Dec){return "PVS1 is not applicable for this variant type.";}
        if ("NF1".equals(PVS1Dec)){return "Nonsense or frameshift -> Predicted to undergo NMD -> Exon is present in biogically-relevent transcript(s) -> PVS1";}
        if ("NF2".equals(PVS1Dec)){return "Nonsense or frameshift -> Predicted to NMD -> Exon is absent in biogically-relevent transcript(s) -> Unmet";}
        if ("NF3".equals(PVS1Dec)){return "Nonsense or frameshift -> Not predicted to NMD -> Truncated/altered region is critical to protein function -> PVS1_Strong";}
        if ("NF4".equals(PVS1Dec)){return "Nonsense or frameshift -> Not predicted to NMD -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in general population and/or exon is absent from biologically-relevant transcript(s) -> Unmet";}
        if ("NF5".equals(PVS1Dec)){return "Nonsense or frameshift -> Not predicted to NMD -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in general population and exon is present from biologically-relevant transcript(s) -> Variant removes >10% of protein -> PVS1_Strong";}
        if ("NF6".equals(PVS1Dec)){return "Nonsense or frameshift -> Not predicted to NMD -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in general population and exon is present from biologically-relevant transcript(s) -> Variant removes <10% of protein -> PVS1_Moderate";}
        if ("SS1".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is predicted to undergo NMD -> Exon is present in biologically-relevant transcript(s) -> PVS1";}
        if ("SS2".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is predicted to undergo NMD -> Exon is absent in biologically-relevant transcript(s) -> Unmet";}
        if ("SS3".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is NOT predicted to undergo NMD -> Truncated/altered region is critical to protein functionc -> PVS1_Strong";}
        if ("SS4".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is NOT predicted to undergo NMD -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in the general population and/or exon is absent from biologically-relevant transcrip(s) -> Unmet";}
        if ("SS5".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is NOT predicted to undergo NMD -> LoF variants in this exon are not frequent in the general population and exon is present in biologically-relevant trancript(s) -> Variant removes >10% of protein -> PVS1_Strong";}
        if ("SS6".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site disrupts reading frame and is NOT predicted to undergo NMD -> LoF variants in this exon are not frequent in the general population and exon is present in biologically-relevant trancript(s) -> Variant removes <10% of protein -> PVS1_Moderate";}
        if ("SS7".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site preserves reading frame -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in the general population and/or exon is absent from biologically-relevant transcrip(s) -> Unmet";}
        if ("SS8".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site preserves reading frame -> Role of region in protein function is unknown -> LoF variants in this exon are not frequent in the general population and exon is present in biologically-relevant trancript(s) -> Variant removes >10% of protein -> PVS1_Strong";}
        if ("SS9".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site preserves reading frame -> Role of region in protein function is unknown -> LoF variants in this exon are not frequent in the general population and exon is present in biologically-relevant trancript(s) -> Variant removes <10% of protein -> PVS1_Moderate";}
        if ("SS10".equals(PVS1Dec)){return "GT-AG 1,2 splice sites -> Exon skipping or use of a cryptic splice site preserves reading frame -> Truncated/altered region is critical to protein function -> PVS1_Strong";}
        if ("DEL1".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Full gene deletion -> PVS1";}
        if ("DEL2".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is predicted to undergo NMD -> Exon is present in biogically-relevent transcript(s) -> PVS1";}
        if ("DEL3".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is predicted to undergo NMD -> Exon is absent in biogically-relevent transcript(s) -> Unmet";}
        if ("DEL4".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is NOT predicted to undergo NMD -> Truncated/altered region is critical to protein functionc -> PVS1_Strong";}
        if ("DEL5".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is NOT predicted to undergo NMD -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in the general population and/or exon is absent from biologically-relevant transcript(s) -> Unmet";}
        if ("DEL6".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is NOT predicted to undergo NMD -> Role of region in protein function is unknown -> Variant removes >10% of protein -> PVS1_Strong";}
        if ("DEL7".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Disrupts reading frame and is NOT predicted to undergo NMD -> Role of region in protein function is unknown -> Variant removes <10% of protein -> PVS1_Moderate";}
        if ("DEL8".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Preserves reading frame -> Truncated/altered region is critical to protein function -> PVS1_Strong";}
        if ("DEL9".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Preserves reading frame -> Role of region in protein function is unknown -> LoF variants in this exon are frequent in the general population and/or exon is absent from biologically-relevant transcript(s) -> Unmet";}
        if ("DEL10".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Preserves reading frame -> Role of region in protein function is unknown -> Variant removes >10% of protein -> PVS1_Strong";}
        if ("DEL11".equals(PVS1Dec)){return "Deletion(single exon to full gene) -> Single to multi exon deletion - Preserves reading frame -> Role of region in protein function is unknown -> Variant removes <10% of protein -> PVS1_Moderate";}
        if ("DUP1".equals(PVS1Dec)){return "Duplication(≥1 exon in size and must be completely contained within gene) -> Proven in tandem -> Reading frame disrupted and NMD predicted to occur -> PVS1";}
        if ("DUP2".equals(PVS1Dec)){return "Duplication(≥1 exon in size and must be completely contained within gene) -> Proven in tandem -> No or unknown impact on reading frame and NMD -> Unmet";}
        if ("DUP3".equals(PVS1Dec)){return "Duplication(≥1 exon in size and must be completely contained within gene) -> Presumed in tandem -> Reading frame presumed disrupted and NMD predicted to occur -> PVS1_Strong";}
        if ("DUP4".equals(PVS1Dec)){return "Duplication(≥1 exon in size and must be completely contained within gene) -> Presumed in tandem -> No or unknown impact on reading frame and NMD -> Unmet";}
        if ("DUP5".equals(PVS1Dec)){return "Duplication(≥1 exon in size and must be completely contained within gene) -> Proven not in tandem -> Unmet";}
        if ("IC1".equals(PVS1Dec)){return "Initiation Codon -> No known alternative start codon in other transcript -> (>6) pathogenic variant(s) upstream of closest potential in-frame start codon -> PVS1";}
        if ("IC2".equals(PVS1Dec)){return "Initiation Codon -> No known alternative start codon in other transcript -> (4~6) pathogenic variant(s) upstream of closest potential in-frame start codon -> PVS1_Strong";}
        if ("IC3".equals(PVS1Dec)){return "Initiation Codon -> No known alternative start codon in other transcript -> (1~3) pathogenic variant(s) upstream of closest potential in-frame start codon -> PVS1_Moderate";}
        if ("IC4".equals(PVS1Dec)){return "Initiation Codon -> No known alternative start codon in other transcript -> No pathogenic variant(s) upstream of closest potential in-frame start codon -> PVS1-Supp";}
        if ("IC5".equals(PVS1Dec)){return "Different functional transcript uses alternative start codon -> Unmet";}
        if ("IC0".equals(PVS1Dec)){return "No in-frame start codon";}
        if ("PTEN".equals(PVS1Dec)){return "PTEN disease specific criterion";}
        if ("CDH1".equals(PVS1Dec)){return "CDH1 disease specific criterion";}
        return Dec;
    }
}
