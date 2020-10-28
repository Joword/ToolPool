package com.bgi.interpretation.modules.sys.utils;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.sun.org.apache.bcel.internal.generic.ARRAYLENGTH;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

/**
 * @Auther: Joword
 * @Date: 2020/9/17 0017 11:14
 * @Description:在python给java传输的时候碰到严谨的数据结构问题，需要将python字典转为java的JSONObject
 * 拿到里面的数据，再转存至新的JSONObject中，其中包含有一层字典以及多层字典的处理
 */
public class String2JSONObject {
    
    public static ArrayList<String> popLists  = new ArrayList<>(Arrays.asList("afr,amr,nfe,fin,asj,eas,sas,oth".split(",")));
    
    public static HashMap populationHashMap(){
        HashMap<String, String> popHashMap = new HashMap<>();
        popHashMap.put("afr","African");
        popHashMap.put("amr","Latino");
        popHashMap.put("asj","Ashkenazi Jewish");
        popHashMap.put("nfe","non-Finnish European");
        popHashMap.put("fin","Finnish");
        popHashMap.put("eas","East Asian");
        popHashMap.put("sas","South Asian");
        popHashMap.put("oth","Other");
        return popHashMap;
    }
    
    public static JSONObject totalJSONObject(JSONObject data, String name){
        
        JSONArray populationDataArray = new JSONArray();
        JSONObject jsonObjectNew = new JSONObject();
        JSONObject jsonObject1 = new JSONObject();
        JSONObject jsonObject2 = new JSONObject();
        JSONObject jsonObject3 = new JSONObject();
        JSONObject jsonObject4 = new JSONObject();
        JSONObject jsonObject5 = new JSONObject();
        JSONObject jsonObject6 = new JSONObject();
        JSONObject jsonObject7 = new JSONObject();
        JSONObject jsonObject8 = new JSONObject();
        
        JSONObject acPOP = JSONObject.parseObject(data.getString("ac_pop"));
        JSONObject anPOP = JSONObject.parseObject(data.getString("an_pop"));
        JSONObject afPOP = JSONObject.parseObject(data.getString("af_pop"));
        JSONObject nhomalt = JSONObject.parseObject(data.getString("nhomalt"));
        
        jsonObject1.put("ac_pop",acPOP.getString("ac_pop_afr"));
        jsonObject1.put("an_pop",anPOP.getString("an_pop_afr"));
        jsonObject1.put("af_pop",afPOP.getString("af_pop_afr"));
        jsonObject1.put("nhomalt",nhomalt.getString("nhomalt_afr"));
        jsonObject1.put("label",populationHashMap().get("afr").toString());
        
        jsonObject2.put("ac_pop",acPOP.getString("ac_pop_amr"));
        jsonObject2.put("an_pop",anPOP.getString("an_pop_amr"));
        jsonObject2.put("af_pop",afPOP.getString("af_pop_amr"));
        jsonObject2.put("nhomalt",nhomalt.getString("nhomalt_amr"));
        jsonObject2.put("label",populationHashMap().get("amr").toString());
        
        jsonObject3.put("ac_pop",acPOP.getString("ac_pop_asj"));
        jsonObject3.put("an_pop",anPOP.getString("an_pop_asj"));
        jsonObject3.put("af_pop",afPOP.getString("af_pop_asj"));
        jsonObject3.put("nhomalt",nhomalt.getString("nhomalt_asj"));
        jsonObject3.put("label",populationHashMap().get("asj").toString());
        
        jsonObject4.put("ac_pop",acPOP.getString("ac_pop_nfe"));
        jsonObject4.put("an_pop",anPOP.getString("an_pop_nfe"));
        jsonObject4.put("af_pop",afPOP.getString("af_pop_nfe"));
        jsonObject4.put("nhomalt",nhomalt.getString("nhomalt_nfe"));
        jsonObject4.put("label",populationHashMap().get("nfe").toString());
        
        jsonObject5.put("ac_pop",acPOP.getString("ac_pop_fin"));
        jsonObject5.put("an_pop",anPOP.getString("an_pop_fin"));
        jsonObject5.put("af_pop",afPOP.getString("af_pop_fin"));
        jsonObject5.put("nhomalt",nhomalt.getString("nhomalt_fin"));
        jsonObject5.put("label",populationHashMap().get("fin").toString());
        
        jsonObject6.put("ac_pop",acPOP.getString("ac_pop_eas"));
        jsonObject6.put("an_pop",anPOP.getString("an_pop_eas"));
        jsonObject6.put("af_pop",afPOP.getString("af_pop_eas"));
        jsonObject6.put("nhomalt",nhomalt.getString("nhomalt_eas"));
        jsonObject6.put("label",populationHashMap().get("eas").toString());
        
        jsonObject7.put("ac_pop",acPOP.getString("ac_pop_sas"));
        jsonObject7.put("an_pop",anPOP.getString("an_pop_sas"));
        jsonObject7.put("af_pop",afPOP.getString("af_pop_sas"));
        jsonObject7.put("nhomalt",nhomalt.getString("nhomalt_sas"));
        jsonObject7.put("label",populationHashMap().get("sas").toString());
        
        jsonObject8.put("ac_pop",acPOP.getString("ac_pop_oth"));
        jsonObject8.put("an_pop",anPOP.getString("an_pop_oth"));
        jsonObject8.put("af_pop",afPOP.getString("af_pop_oth"));
        jsonObject8.put("nhomalt",nhomalt.getString("nhomalt_oth"));
        jsonObject8.put("label",populationHashMap().get("oth").toString());
        
        populationDataArray.add(jsonObject1);
        populationDataArray.add(jsonObject2);
        populationDataArray.add(jsonObject3);
        populationDataArray.add(jsonObject4);
        populationDataArray.add(jsonObject5);
        populationDataArray.add(jsonObject6);
        populationDataArray.add(jsonObject7);
        populationDataArray.add(jsonObject8);
        jsonObjectNew.put(name,populationDataArray);
        return jsonObjectNew;
    }

    public static JSONObject exmoesGenomicsJSONObject(JSONObject data, String name){

        JSONArray populationDataArray = new JSONArray();
        JSONObject jsonObjectNew = new JSONObject();
        JSONObject jsonObject1 = new JSONObject();
        JSONObject jsonObject2 = new JSONObject();
        JSONObject jsonObject3 = new JSONObject();
        JSONObject jsonObject4 = new JSONObject();
        JSONObject jsonObject5 = new JSONObject();
        JSONObject jsonObject6 = new JSONObject();
        JSONObject jsonObject7 = new JSONObject();
        JSONObject jsonObject8 = new JSONObject();
        
        if (data.getString("filter").equals("PASS")){
            JSONObject acPOP = JSONObject.parseObject(data.getString("ac_pop"));
            JSONObject anPOP = JSONObject.parseObject(data.getString("an_pop"));
            JSONObject afPOP = JSONObject.parseObject(data.getString("af_pop"));
            JSONObject nhomalt = JSONObject.parseObject(data.getString("nhomalt"));

            jsonObject1.put("ac_pop",acPOP.getString("afr"));
            jsonObject1.put("an_pop",anPOP.getString("afr"));
            jsonObject1.put("af_pop",afPOP.getString("afr"));
            jsonObject1.put("nhomalt",nhomalt.getString("afr"));
            jsonObject1.put("label",populationHashMap().get("afr").toString());

            jsonObject2.put("ac_pop",acPOP.getString("amr"));
            jsonObject2.put("an_pop",anPOP.getString("amr"));
            jsonObject2.put("af_pop",afPOP.getString("amr"));
            jsonObject2.put("nhomalt",nhomalt.getString("amr"));
            jsonObject2.put("label",populationHashMap().get("amr").toString());

            jsonObject3.put("ac_pop",acPOP.getString("asj"));
            jsonObject3.put("an_pop",anPOP.getString("asj"));
            jsonObject3.put("af_pop",afPOP.getString("asj"));
            jsonObject3.put("nhomalt",nhomalt.getString("asj"));
            jsonObject3.put("label",populationHashMap().get("asj").toString());

            jsonObject4.put("ac_pop",acPOP.getString("nfe"));
            jsonObject4.put("an_pop",anPOP.getString("nfe"));
            jsonObject4.put("af_pop",afPOP.getString("nfe"));
            jsonObject4.put("nhomalt",nhomalt.getString("nfe"));
            jsonObject4.put("label",populationHashMap().get("nfe").toString());

            jsonObject5.put("ac_pop",acPOP.getString("fin"));
            jsonObject5.put("an_pop",anPOP.getString("fin"));
            jsonObject5.put("af_pop",afPOP.getString("fin"));
            jsonObject5.put("nhomalt",nhomalt.getString("fin"));
            jsonObject5.put("label",populationHashMap().get("fin").toString());

            jsonObject6.put("ac_pop",acPOP.getString("eas"));
            jsonObject6.put("an_pop",anPOP.getString("eas"));
            jsonObject6.put("af_pop",afPOP.getString("eas"));
            jsonObject6.put("nhomalt",nhomalt.getString("eas"));
            jsonObject6.put("label",populationHashMap().get("eas").toString());

            jsonObject7.put("ac_pop",acPOP.getString("sas"));
            jsonObject7.put("an_pop",anPOP.getString("sas"));
            jsonObject7.put("af_pop",afPOP.getString("sas"));
            jsonObject7.put("nhomalt",nhomalt.getString("sas"));
            jsonObject7.put("label",populationHashMap().get("sas").toString());

            jsonObject8.put("ac_pop",acPOP.getString("oth"));
            jsonObject8.put("an_pop",anPOP.getString("oth"));
            jsonObject8.put("af_pop",afPOP.getString("oth"));
            jsonObject8.put("nhomalt",nhomalt.getString("oth"));
            jsonObject8.put("label",populationHashMap().get("oth").toString());

            populationDataArray.add(jsonObject1);
            populationDataArray.add(jsonObject2);
            populationDataArray.add(jsonObject3);
            populationDataArray.add(jsonObject4);
            populationDataArray.add(jsonObject5);
            populationDataArray.add(jsonObject6);
            populationDataArray.add(jsonObject7);
            populationDataArray.add(jsonObject8);
            jsonObjectNew.put(name,populationDataArray);
        }else if (!data.getString("filter").equals("PASS")){
            jsonObjectNew = data;
        }
        return jsonObjectNew;
    }
    
    public static JSONObject popDataFormat(JSONObject total, JSONObject exmoes, JSONObject genomics){
        //exmoes, genomics, total三组数据中ac_pop的数据
        JSONObject jsonObject = new JSONObject();
        JSONObject totalJSONObject = totalJSONObject(total,"total");
        JSONObject exmoesJSONObject = exmoesGenomicsJSONObject(exmoes,"exmoes");
        JSONObject genomicsJSONObject = exmoesGenomicsJSONObject(genomics,"genomics");

        jsonObject.put("total",totalJSONObject.getJSONArray("total"));
        jsonObject.put("exmoes",exmoesJSONObject.getJSONArray("exmoes"));
        jsonObject.put("genomics",genomicsJSONObject.getJSONArray("genomics"));
        return jsonObject;
    }
    
}
