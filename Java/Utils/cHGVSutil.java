package com.bgi.interpretation.modules.sys.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @Auther: Joword
 * @Date: 2020/6/15 0015 20:44
 * @Description:为咗俾googleAlert，减短回调时间，缩短前端反应时间，要将python处理cHGVS噶正则匹配改写为java式，唔该仁慈的独裁者对人类噶贡献
 */
public class cHGVSutil {
    
    /*已找到的cHGVS情况共计10种，GJB3 c.124C>T/SLC26A4 c.-103T>C/CLRN1 c.149_152delCAGGinsTGTCCAAT/
    CLRN1 c.301_305delGTCAT/OTOF c.699delA/USH2A c.6486-26_6499delATAATAATGTATTTTACCATTCCCAGGTGGAAACAACCAA/
    GJB2 c.-22-12C>T/DFNA5 c.1183+1delG/DIABLO c.-805-u5396C>T, CLRN1 c.433+2_433+3insT, FGFR3 c.444_445+2delAGGG/intron
    * */
    public static String[] regularExp(String chgvs, String intron){
        Pattern snv1Pattern = Pattern.compile("c\\.(?<cpos>\\d+)(?<ref>[ATCG])>(?<alt>[ATCG])", Pattern.CASE_INSENSITIVE);
        Pattern snv2Pattern = Pattern.compile("c\\.([\\-\\*])(\\d+)([ATCG])>([ATCG])", Pattern.CASE_INSENSITIVE);
        Pattern delinPattern = Pattern.compile("c\\.(\\d+)_(\\d+)del([ATCG]+)ins([ATCG]+)", Pattern.CASE_INSENSITIVE);
        Pattern indel1Pattern = Pattern.compile("c\\.(\\d+)_(\\d+)(ins|del|dup)([ATCG]*)",Pattern.CASE_INSENSITIVE);
        Pattern indel2Pattern = Pattern.compile("c\\.(\\d+)(ins|del|dup)([ATCG]*)", Pattern.CASE_INSENSITIVE);
        Pattern indel3Pattern = Pattern.compile("c\\.(\\d+(?:[\\+\\-‐–]\\d+)?_\\d+(?:[\\+-]\\d+)?del)([ATCG]*)", Pattern.CASE_INSENSITIVE);
        Pattern splice1Pattern = Pattern.compile("c\\.([\\+\\-]?)(\\d+)([\\+\\-‐–])(\\d+)([ATCG]+)>([ATCG]+)", Pattern.CASE_INSENSITIVE);
        Pattern splice2Pattern = Pattern.compile("c\\.(\\d+)([\\+\\-‐–])(\\d+)(ins|del|dup)([ATCG]+)", Pattern.CASE_INSENSITIVE);
        Pattern allcHGVSPattern = Pattern.compile("c\\.([\\d*\\+\\-_>(?:dup|ins|del)ATCG]+)", Pattern.CASE_INSENSITIVE);
        Pattern intronPattern = Pattern.compile("(\\d+)(?:/(\\d+))?", Pattern.CASE_INSENSITIVE);

        Matcher snv1Matcher = snv1Pattern.matcher(chgvs);
        Matcher snv2Matcher = snv2Pattern.matcher(chgvs);
        Matcher delinMatcher = delinPattern.matcher(chgvs);
        Matcher indel1Matcher = indel1Pattern.matcher(chgvs);
        Matcher indel2Matcher = indel2Pattern.matcher(chgvs);
        Matcher indel3Matcher = indel3Pattern.matcher(chgvs);
        Matcher splice1Matcher = splice1Pattern.matcher(chgvs);
        Matcher splice2Matcher = splice2Pattern.matcher(chgvs);
        Matcher allcHGVSMatcher = allcHGVSPattern.matcher(chgvs);
        Matcher intronMatcher = intronPattern.matcher(intron);
        
        String[] allcHGVS = new String[10];
        String[] allcHGVSSnv1 = new String[2];
        String[] allcHGVSSnv2 = new String[2];
        String[] allcHGVSDelin = new String[5];
        
        if (snv1Matcher.matches()){
            String pos = snv1Matcher.group("cpos");
            String ref = snv1Matcher.group("ref");
            String alt = snv1Matcher.group("alt");
            allcHGVSSnv1[0] = pos + ref + '>' + alt;
            allcHGVSSnv1[1] = ref + pos + alt;
        }else if (snv2Matcher.matches()){
            String utr = snv2Matcher.group(0);
            String pos = snv2Matcher.group(1);
            String ref = snv2Matcher.group(2);
            String alt = snv2Matcher.group(3);
            allcHGVSSnv2[1] = '-' + pos + ref + '>' + alt;
            allcHGVSSnv2[2] = ref + '-' + pos + alt;
        }else if (delinMatcher.matches()){
            String pos1 = delinMatcher.group(0);
            String pos2 = delinMatcher.group(1);
            String base1 = delinMatcher.group(2);
            String base2 = delinMatcher.group(3);
            Integer length = Integer.parseInt(pos2) - Integer.parseInt(pos1) + 1;
            
        }
        return allcHGVS;
    }
    
}
