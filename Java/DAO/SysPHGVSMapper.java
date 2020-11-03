package com.bgi.interpretation.modules.sys.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.bgi.interpretation.modules.sys.po.SysSearchTest;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * @author mengjunhua
 * @Auther: Joword
 * @Date: 2020/11/3 0003 09:31
 * @Description:
 */
public interface SysPHGVSMapper extends BaseMapper<SysSearchTest> {
    /**从数据库获取gene和pHGVS，以便与前端比较
     * @param gene 数据库基因
     * @param phgvs 数据库phgvs
     * @return None
     */
    List<SysSearchTest> getSysPHGVSByGenepHGVS(@Param("gene") String gene, @Param("phgvs") String phgvs);

    /**从数据库获取转录本和pHGVS，以便与前端比较
     * @param transcriptp 数据库转录本
     * @param phgvs 数据库pHGVS
     * @return None
     */
    List<SysSearchTest> getTranscriptpHGVSList(@Param("transcriptp") String transcriptp, @Param("phgvs") String phgvs);
}
