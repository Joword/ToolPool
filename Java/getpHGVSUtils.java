package com.bgi.interpretation.modules.sys.utils;

import java.util.regex.Pattern;

/**
 * @Auther: Joword
 * @Date: 2020/6/23 0023 12:05
 * @Description:处理PS1、PM5证据项pHGVS问题
 */
public class getpHGVSUtils  {
    
    public static String stringBuffer2String(String arg){
        final String BARRMARK = "-";

        StringBuffer pHGVSBuffer = new StringBuffer();
        if (!arg.equals(BARRMARK)){
            pHGVSBuffer.append(arg.split(":")[1]);
        }else {
            pHGVSBuffer.append(BARRMARK);
        }
        return pHGVSBuffer.toString();
    }
    
    public static String[] pHGVSLocation(String arg){
        String pHGVS = stringBuffer2String(arg);
        final  String BARRMARK = "-";
        
        String[] pHGVSs = new String[2];
        if (!pHGVS.equals(BARRMARK)){
            pHGVSs[1] = pHGVS.substring(pHGVS.length()-3,pHGVS.length());
            pHGVSs[0] = pHGVS.substring(0, pHGVS.length()-3);
        }
        return pHGVSs;
    }
    
    public static String[] cHGVSLocation(String arg){
        String cHGVS = stringBuffer2String(arg);
        final String BARRMARK = "-";
        
        String[] cHGVSs = new String[4];
        if (!cHGVS.equals("-")){
            cHGVSs[0] = cHGVS.substring(cHGVS.length()-1,cHGVS.length());
            cHGVSs[1] = cHGVS.substring(cHGVS.length()-5,cHGVS.length()-3);
            cHGVSs[2] = cHGVS.substring(cHGVS.length()-6,cHGVS.length()-3);
            cHGVSs[3] = cHGVS.substring(0,cHGVS.length()-2);
        }
        return cHGVSs;
    }
}
