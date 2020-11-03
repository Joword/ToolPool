package com.bgi.interpretation.modules.sys.service.serviceimpl;

import com.bgi.interpretation.modules.sys.mapper.SysPHGVSMapper;
import com.bgi.interpretation.modules.sys.po.SysSearchTest;
import com.bgi.interpretation.modules.sys.service.ISysPHGVSSearchService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author : Joword
 * @Date: 2020/11/3 0003 09:45
 * @Description:pHGVS模糊搜索实现类
 */
@Service
public class ISysPHGVSSearchServiceImpl implements ISysPHGVSSearchService {
    @Resource
    SysPHGVSMapper sysPHGVSMapper;
    
    @Override
    public List<SysSearchTest> getGenepHGVSList(String gene, String phgvs) { return sysPHGVSMapper.getSysPHGVSByGenepHGVS(gene, phgvs); }
    
    @Override
    public List<SysSearchTest> getTranscriptpHGVSList(String transcriptp, String phgvs){ return sysPHGVSMapper.getTranscriptpHGVSList(transcriptp, phgvs); };
}
