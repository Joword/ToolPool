package com.bgi.interpretation.modules.sys.utils;

import java.lang.reflect.Array;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.alibaba.fastjson.JSONObject;
import io.swagger.models.auth.In;

/**
 * @Auther: Joword
 * @Date: 2020/7/21 0021 16:28
 * @Description:
 */
public class AminoAcidUtils {
    
    /*氨基酸-氨基酸简写*/
    public static String aminoAcid2Abbreviation(String arg){
        String aminoAcidString = "{'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K','Trp': 'W', 'Thr': 'T', 'Asn': 'N', 'Pro': 'P', 'Phe': 'F','Ala': 'A', 'Gly': 'G', 'Ile': 'I', 'Leu': 'L', 'His': 'H','Arg': 'R', 'Met': 'M', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y','Sec': 'U', 'Pyl': 'O', 'Ter': '*'}";
        return (String) JSONObject.parseObject(JSONObject.parseObject(aminoAcidString).toJSONString()).get(arg);
    }

    /*氨基酸简写-氨基酸*/
    public static String abbreviation2AminoAcid(String arg){
        String amninoAcidAbbrString = "{'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys','W': 'Trp', 'T': 'Thr', 'N': 'Asn', 'P': 'Pro', 'F': 'Phe','A': 'Ala', 'G': 'Gly', 'I': 'Ile', 'L': 'Leu', 'H': 'His','R': 'Arg', 'M': 'Met', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr','*': 'Ter', 'X': 'Ter'}";
        return (String) JSONObject.parseObject(JSONObject.parseObject(amninoAcidAbbrString).toJSONString()).get(arg);
    }
    
    public static String aa2AbbrMatch(String arg){
        /*输入phgvs返回phgvs缩写*/
        String aminoAcidString = "{'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K','Trp': 'W', 'Thr': 'T', 'Asn': 'N', 'Pro': 'P', 'Phe': 'F','Ala': 'A', 'Gly': 'G', 'Ile': 'I', 'Leu': 'L', 'His': 'H','Arg': 'R', 'Met': 'M', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y','Sec': 'U', 'Pyl': 'O', 'Ter': '*'}";
        JSONObject aa2AbbrJson = JSONObject.parseObject(JSONObject.parseObject(aminoAcidString).toJSONString());
        /*hashSet转list一样可以打到数组的效果*/
        Set<String> aa2AbbreviationKeySet = new HashSet<>(aa2AbbrJson.keySet());
        List<String> aa2AbbreviationKeyList = new ArrayList<>(aa2AbbreviationKeySet);
        for (String value : aa2AbbreviationKeyList) {
            Pattern aa2AbbreviationPattern = Pattern.compile(value, Pattern.CASE_INSENSITIVE);
            Matcher aa2AbbreviationMatcher = aa2AbbreviationPattern.matcher(arg);
            if (aa2AbbreviationMatcher.find()) { arg = arg.replace(value, (CharSequence) aa2AbbrJson.get(value)); }
        }
        return arg;
    }

    public static String abbr2AAMatch(String arg){
        /*输入phgvs缩写返回phgvs*/
        String amninoAcidAbbrString = "{'C': 'Cys', 'D': 'Asp', 'S': 'Ser', 'Q': 'Gln', 'K': 'Lys','W': 'Trp', 'T': 'Thr', 'N': 'Asn', 'P': 'Pro', 'F': 'Phe','A': 'Ala', 'G': 'Gly', 'I': 'Ile', 'L': 'Leu', 'H': 'His','R': 'Arg', 'M': 'Met', 'V': 'Val', 'E': 'Glu', 'Y': 'Tyr','*': 'Ter', 'X': 'Ter'}";
        JSONObject aa2AbbrJson = JSONObject.parseObject(JSONObject.parseObject(amninoAcidAbbrString).toJSONString());
        /*hashSet转list一样可以打到数组的效果*/
        Set<String> aa2AbbreviationKeySet = new HashSet<>(aa2AbbrJson.keySet());
        List<String> aa2AbbreviationKeyList = new ArrayList<>(aa2AbbreviationKeySet);
        for (String value : aa2AbbreviationKeyList) {
            Pattern aa2AbbreviationPattern = Pattern.compile(value, Pattern.CASE_INSENSITIVE);
            Matcher aa2AbbreviationMatcher = aa2AbbreviationPattern.matcher(arg);
            if (aa2AbbreviationMatcher.find()) { arg = arg.replace(value, (CharSequence) aa2AbbrJson.get(value)); }
        }
        return arg;
    }
}
