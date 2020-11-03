package com.bgi.interpretation.modules.sys.service;

import com.bgi.interpretation.modules.sys.po.SysSearchTest;

import java.util.List;

/**
 * @author Joword
 * @Date: 2020/11/3 0003 09:45
 * @Description:
 */
public interface ISysPHGVSSearchService {
    /**服务层的接口类，与实现类相配套，承接DAO层
     * @param gene 数据库基因
     * @param phgvs 数据库pHGVS
     * @return None
     */
    List<SysSearchTest> getGenepHGVSList(String gene, String phgvs);

    /**服务层的接口类，与实现类相配套，承接DAO层
     * @param transcriptp 数据库转录本
     * @param phgvs 数据库pHGVS
     * @return
     */
    List<SysSearchTest> getTranscriptpHGVSList(String transcriptp, String phgvs);
}
