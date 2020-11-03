package com.bgi.interpretation.modules.sys.utils;

import com.alibaba.fastjson.JSONObject;
import com.bgi.interpretation.modules.sys.po.PmidInformation;

import java.util.*;

/**
 * @Auther: Joword
 * @Date: 2020/8/3 0003 11:25
 * @Description:
 */
public class variantLiteratureUtils {
    
    public static ArrayList<PmidInformation> literatureDifference(List<PmidInformation> oldPMID, List<PmidInformation> PMIDNew){
        /*输入旧文献列表对象与新文献列表对象，求交集与差集，合并返回新文献列表对象给前端*/
        JSONObject oldPmidLiterature = new JSONObject();
        JSONObject pmidLiteratureNew = new JSONObject();
        Set<String> pmidSetRemoveAll = new HashSet<>();
        Set<String> pmidSetRetainAll = new HashSet<>();
        ArrayList<PmidInformation> pmidArrayList = new ArrayList<>();
        if (oldPMID != null && PMIDNew != null){
            for (PmidInformation old:oldPMID){
                JSONObject oldPmidJSONObject = JSONObject.parseObject(JSONObject.toJSONString(old));
                String oldPmidJSONObjectRest = oldPmidJSONObject.get("journalTitle").toString()+"|"+oldPmidJSONObject.get("firstAuthor").toString()+"|"+oldPmidJSONObject.get("year")+"|"+oldPmidJSONObject.get("articleTitle").toString();
                oldPmidLiterature.put(oldPmidJSONObject.get("pmid").toString(),oldPmidJSONObjectRest);
                
            }
            for (PmidInformation pmidNew:PMIDNew){
                JSONObject pmidJSONObjectNew = JSONObject.parseObject(JSONObject.toJSONString(pmidNew));
                String pmidJSONObjectNewRest = pmidJSONObjectNew.get("journalTitle").toString()+"|"+pmidJSONObjectNew.get("firstAuthor")+"|"+pmidJSONObjectNew.get("year").toString()+"|"+pmidJSONObjectNew.get("articleTitle").toString();
                pmidLiteratureNew.put(pmidJSONObjectNew.get("pmid").toString(),pmidJSONObjectNewRest);
            }
            pmidSetRemoveAll.addAll(pmidLiteratureNew.keySet());
            pmidSetRetainAll.addAll(pmidLiteratureNew.keySet());
            pmidSetRemoveAll.removeAll(oldPmidLiterature.keySet());
            pmidSetRetainAll.retainAll(oldPmidLiterature.keySet());
        }
        if (pmidSetRetainAll.size() > 0){
            for(String retainSet:pmidSetRetainAll){
                PmidInformation pmidTemp = new PmidInformation();
                List pmidList = Arrays.asList(pmidLiteratureNew.get(retainSet).toString().split("\\|"));
                pmidTemp.setPmid(retainSet);
                pmidTemp.setJournalTitle(pmidList.get(0).toString());
                pmidTemp.setFirstAuthor(pmidList.get(1).toString());
                pmidTemp.setYear(pmidList.get(2).toString());
                pmidTemp.setArticleTitle(pmidList.get(3).toString());
                pmidTemp.setStatus("Both");
                pmidArrayList.add(pmidTemp);
            }
        }
        if (pmidSetRemoveAll.size() > 0) {
            for (String set:pmidSetRemoveAll){
                PmidInformation pmidTemp = new PmidInformation();
                List pmidList = Arrays.asList(pmidLiteratureNew.get(set).toString().split("\\|"));
                pmidTemp.setPmid(set);
                pmidTemp.setJournalTitle(pmidList.get(0).toString());
                pmidTemp.setFirstAuthor(pmidList.get(1).toString());
                pmidTemp.setYear(pmidList.get(2).toString());
                pmidTemp.setArticleTitle(pmidList.get(3).toString());
                pmidTemp.setStatus("Diff");
                pmidArrayList.add(pmidTemp);
            }
        }
        return pmidArrayList;
    }
    
    public static ArrayList<PmidInformation> fullPmidInformation(List<PmidInformation> pmidOlds,List<PmidInformation> pmidNews){
        JSONObject oldPmidLiterature = new JSONObject();
        JSONObject pmidLiteratureNew = new JSONObject();
        Set<String> pmidSetRemoveAll = new HashSet<>();
        Set<String> pmidSetRetainAll = new HashSet<>();
        Set<String> oldPmidSetRemoveAll = new HashSet<>();
        ArrayList<PmidInformation> pmidArrayList = new ArrayList<>();
        if (pmidOlds != null && pmidNews != null){
            for (PmidInformation old:pmidOlds){
                JSONObject oldPmidJSONObject = JSONObject.parseObject(JSONObject.toJSONString(old));
                String oldPmidJSONObjectRest = oldPmidJSONObject.get("journalTitle").toString()+"|"+oldPmidJSONObject.get("firstAuthor").toString()+"|"+oldPmidJSONObject.get("year")+"|"+oldPmidJSONObject.get("articleTitle").toString();
                oldPmidLiterature.put(oldPmidJSONObject.get("pmid").toString(),oldPmidJSONObjectRest);

            }
            for (PmidInformation pmidNew:pmidNews){
                JSONObject pmidJSONObjectNew = JSONObject.parseObject(JSONObject.toJSONString(pmidNew));
                String pmidJSONObjectNewRest = pmidJSONObjectNew.get("journalTitle").toString()+"|"+pmidJSONObjectNew.get("firstAuthor")+"|"+pmidJSONObjectNew.get("year").toString()+"|"+pmidJSONObjectNew.get("articleTitle").toString();
                pmidLiteratureNew.put(pmidJSONObjectNew.get("pmid").toString(),pmidJSONObjectNewRest);
            }
            pmidSetRemoveAll.addAll(pmidLiteratureNew.keySet());
            pmidSetRetainAll.addAll(pmidLiteratureNew.keySet());
            oldPmidSetRemoveAll.addAll(oldPmidLiterature.keySet());
            pmidSetRemoveAll.removeAll(oldPmidLiterature.keySet());
            pmidSetRetainAll.retainAll(oldPmidLiterature.keySet());
            oldPmidSetRemoveAll.removeAll(pmidLiteratureNew.keySet());
        }
        if (oldPmidSetRemoveAll.size() > 0){
            for (String oldPmid:oldPmidSetRemoveAll){
                PmidInformation pmidTemp = new PmidInformation();
                List pmidList = Arrays.asList(oldPmidLiterature.get(oldPmid).toString().split("\\|"));
                pmidTemp.setPmid(oldPmid);
                pmidTemp.setJournalTitle(pmidList.get(0).toString());
                pmidTemp.setFirstAuthor(pmidList.get(1).toString());
                pmidTemp.setYear(pmidList.get(2).toString());
                pmidTemp.setArticleTitle(pmidList.get(3).toString());
                pmidTemp.setStatus("Old");
                pmidArrayList.add(pmidTemp);
            }
        }
        if (pmidSetRetainAll.size() > 0){
            for(String retainSet:pmidSetRetainAll){
                PmidInformation pmidTemp = new PmidInformation();
                List pmidList = Arrays.asList(pmidLiteratureNew.get(retainSet).toString().split("\\|"));
                pmidTemp.setPmid(retainSet);
                pmidTemp.setJournalTitle(pmidList.get(0).toString());
                pmidTemp.setFirstAuthor(pmidList.get(1).toString());
                pmidTemp.setYear(pmidList.get(2).toString());
                pmidTemp.setArticleTitle(pmidList.get(3).toString());
                pmidTemp.setStatus("Both");
                pmidArrayList.add(pmidTemp);
            }
        }
        if (pmidSetRemoveAll.size() > 0) {
            for (String set:pmidSetRemoveAll){
                PmidInformation pmidTemp = new PmidInformation();
                List pmidList = Arrays.asList(pmidLiteratureNew.get(set).toString().split("\\|"));
                pmidTemp.setPmid(set);
                pmidTemp.setJournalTitle(pmidList.get(0).toString());
                pmidTemp.setFirstAuthor(pmidList.get(1).toString());
                pmidTemp.setYear(pmidList.get(2).toString());
                pmidTemp.setArticleTitle(pmidList.get(3).toString());
                pmidTemp.setStatus("Diff");
                pmidArrayList.add(pmidTemp);
            }
        }
        return pmidArrayList;
    }
    
}
