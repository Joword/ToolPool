package com.bgi.interpretation.modules.sys.utils;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @Auther: Joword
 * @Date: 2020/7/28 0028 16:05
 * @Description:
 */
public class highLightUtils {

    public static String replaceSpacePlus(String evidence){
        return evidence.replace(" + ","+");
    }
    
    public static String replaceSpaceDEL(String evidence){
        return evidence.replace(" del ", "del");
    }
    
    public static String replaceGeneLabel(String gene, String evidence){
        return evidence.replace(gene,"<span class='table-gene-backgroud'>"+gene+"</span>");
    }
    
    public static String replaceHighLightText(String[] text, String evidence){
        if (text.length > 0){
            for (String s:text){
                Pattern textPattern = Pattern.compile("\\b"+s+"\\b");
                Matcher textMatcher = textPattern.matcher(evidence);
                if (textMatcher.find()){
                    evidence = evidence.replace(s,"<span class='table-green-backgroud'>" + s + "</span>");
                }
            }  
        }
        return evidence;
    }
    
    public static String replacePhetnoype(String phenotype,String evidence){
        if (!phenotype.contains(",")){
            if (!phenotype.contains(" ")){
                evidence = evidence.replace(phenotype,"<span class='table-phenotype-backgroud'>" + phenotype + "</span>");
            }else {
                String[] evidenceArray = phenotype.split(" ");
                StringBuffer evidenceFirstName = new StringBuffer();
                List<String> conjunctionArray = Arrays.asList("and", "or", "but", "And", "Or", "But", "If", "if", "though", "Though");
                for (String s:evidenceArray){
                    evidenceFirstName.append(s.substring(0,1).toUpperCase());
                    if (!conjunctionArray.contains(s)){
                        evidence = evidence.replace(s, "<span class='table-phenotype-backgroud'>" + s + "</span>");
                    }
                }
                evidence = evidence.replace(evidenceFirstName.toString(),"<span class='table-phenotype-backgroud'>" + evidenceFirstName.toString() + "</span>");
            }
        }
        if (phenotype.contains(",")){
            for (String s: phenotype.split(",")){
                
                s = s.replace(" ","");
                evidence = evidence.replace(s,"<span class='table-phenotype-backgroud'>" + s + "</span>");
            }
        }
        return evidence;
    }
    
    public static String replaceExperiment(String experiments,String evidence){
        if (experiments.contains(" || ")){
            Set<String> experiment = new HashSet<String>(Arrays.asList(experiments.split(" \\|\\| ")));
            List<String> experimentList = new ArrayList<>(experiment);
            for (String s:experimentList){
                if (s.contains(",")){
                    String[] singleExperiment = s.split(",");
                    for (String se: singleExperiment){
                        se = se.replace(" ","");
                        evidence = evidence.replace(se,"<span class='table-experiment-backgroud'>" + se + "</span>");
                    }
                }else {
                    evidence = evidence.replace(s,"<span class='table-experiment-backgroud'>" + s + "</span>");
                }
            }
        }else if (experiments.contains(",")){
            String[] experiment = experiments.split(",");
            for (String s:experiment){
                s = s.replace(" ","");
                evidence = evidence.replace(s,"<span class='table-experiment-backgroud'>" + s + "</span>");
            }
        }else {
            evidence = evidence.replace(experiments,"<span class='table-experiment-backgroud'>" + experiments + "</span>");
        }
        return evidence;
    }

    public static String replaceFunctionChange(String funcChange,String evidence){
        if (funcChange.contains(" || ")){
            Set<String> fChange = new HashSet<String>(Arrays.asList(funcChange.split(" \\|\\| ")));
            List<String> fChangeList = new ArrayList<>(fChange);
            for (String s:fChangeList){
                if (s.contains(",")){
                    String[] singleExperiment = s.split(",");
                    for (String se: singleExperiment){
                        se = se.replace(" ","");
                        evidence = evidence.replace(se,"<span class='table-funChange-backgroup'>" + se + "</span>");
                    }
                }else {
                    evidence = evidence.replace(s,"<span class='table-funChange-backgroup'>" + s + "</span>");
                }
            }
        }else if (funcChange.contains(",")){
            String[] funChange = funcChange.split(",");
            for (String fc:funChange){
                fc = fc.replace(" ","");
                evidence = evidence.replace(fc,"<span class='table-funChange-backgroup'>" + fc + "</span>");
            }
        }else {
            evidence = evidence.replace(funcChange,"<span class='table-funChange-backgroup'>" + funcChange + "</span>");
        }
        return evidence;
    }
    
}
