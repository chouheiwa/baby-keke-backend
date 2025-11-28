from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta

from wxcloudrun import schemas
from wxcloudrun.crud import vaccine as vaccine_crud
from wxcloudrun.crud import baby as baby_crud
from wxcloudrun.core.database import get_db
from wxcloudrun.routers.auth import get_current_user_id

router = APIRouter(
    prefix="/api",
    tags=["vaccines"]
)

# === 疫苗基础数据 ===

@router.get("/vaccines", response_model=List[schemas.vaccine.Vaccine])
def get_vaccines(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """获取所有疫苗列表"""
    return vaccine_crud.get_vaccines(db, active_only)

@router.post("/vaccines/init")
def init_vaccines(
    db: Session = Depends(get_db)
):
    """初始化疫苗数据（内部使用）"""
    # 这里定义标准疫苗数据
    # 1类免费疫苗
    # 1类免费疫苗
    free_vaccines = [
        {
            "name": "乙肝疫苗", "code": "HepB", "dose_seq": 1, "type": "FREE", "target_age_month": 0,
            "description": "出生后24小时内接种",
            "side_effects": "注射部位可能出现红肿、硬结；少数宝宝可能出现低热、疲倦等症状，一般1-2天自行消退。",
            "precautions": "接种前告知医生宝宝健康状况；接种后留观30分钟，注意观察宝宝反应；当天避免洗澡，保持接种部位清洁干燥。",
            "contraindications": "对酵母过敏者禁用；急性疾病、严重慢性疾病、过敏体质者暂缓接种。",
            "interval_info": "第1剂与第2剂间隔≥28天"
        },
        {
            "name": "卡介苗", "code": "BCG", "dose_seq": 1, "type": "FREE", "target_age_month": 0,
            "description": "出生时接种，预防结核病",
            "side_effects": "接种后2-3周局部出现红肿硬结，随后可能化脓、溃烂，8-12周自愈并留下疤痕，这是正常反应。",
            "precautions": "接种后不能搓揉接种部位；化脓期注意局部清洁，避免感染；接种侧腋窝淋巴结可能肿大，一般3个月内自行消退。",
            "contraindications": "早产儿、低体重儿(<2500g)、免疫缺陷、结核病患者禁用。",
            "interval_info": "仅接种1剂"
        },
        {
            "name": "乙肝疫苗", "code": "HepB", "dose_seq": 2, "type": "FREE", "target_age_month": 1, 
            "description": "第2剂",
            "side_effects": "同第1剂，反应通常较轻。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "第2剂与第3剂间隔≥60天"
        },
        {
            "name": "脊灰疫苗(IPV)", "code": "IPV", "dose_seq": 1, "type": "FREE", "target_age_month": 2,
            "description": "预防脊髓灰质炎",
            "side_effects": "注射部位可能红肿、疼痛；极少数出现发热、烦躁不安。",
            "precautions": "接种后观察30分钟；注意观察宝宝体温变化；保持接种部位清洁。",
            "contraindications": "对疫苗成分过敏者；急性疾病期、发热者暂缓接种。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "脊灰疫苗(IPV)", "code": "IPV", "dose_seq": 2, "type": "FREE", "target_age_month": 3, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "百白破疫苗", "code": "DTaP", "dose_seq": 1, "type": "FREE", "target_age_month": 3,
            "description": "预防百日咳、白喉、破伤风",
            "side_effects": "注射部位红肿、硬结、疼痛；部分宝宝可能发热、烦躁、食欲减退；极少数出现高热、惊厥。",
            "precautions": "接种前告知医生既往过敏史；接种后观察30分钟；注意观察体温，如发热超过38.5℃需就医；避免剧烈运动。",
            "contraindications": "有癫痫、惊厥史者；急性疾病、发热者；过敏体质者；免疫缺陷者暂缓接种。前一次接种后出现高热、惊厥者慎用。",
            "interval_info": "基础免疫3剂，各剂间隔≥28天；加强免疫与基础免疫间隔≥6个月"
        },
        {
            "name": "脊灰疫苗(OPV/IPV)", "code": "OPV", "dose_seq": 3, "type": "FREE", "target_age_month": 4, 
            "description": "第3剂，口服", 
            "administration_route": "ORAL",
            "side_effects": "口服后一般无不良反应，少数可能出现轻度腹泻。",
            "precautions": "口服前后30分钟避免喂奶、喝热水；注意观察有无呕吐。",
            "contraindications": "免疫缺陷者禁用（应改用IPV）；急性疾病、发热者暂缓。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "百白破疫苗", "code": "DTaP", "dose_seq": 2, "type": "FREE", "target_age_month": 4, 
            "description": "第2剂",
            "side_effects": "同第1剂，局部反应可能随剂次增加而加重。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "百白破疫苗", "code": "DTaP", "dose_seq": 3, "type": "FREE", "target_age_month": 5, 
            "description": "第3剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "乙肝疫苗", "code": "HepB", "dose_seq": 3, "type": "FREE", "target_age_month": 6, 
            "description": "第3剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "A群流脑疫苗", "code": "MenA", "dose_seq": 1, "type": "FREE", "target_age_month": 6, 
            "description": "预防A群流行性脑脊髓膜炎",
            "side_effects": "注射部位轻微红肿、疼痛；少数出现低热，一般1-2天消退。",
            "precautions": "接种后观察30分钟；注意多喝水，休息。",
            "contraindications": "对疫苗成分过敏者；癫痫、惊厥史者；急性疾病、发热者暂缓。",
            "interval_info": "第1剂与第2剂间隔≥3个月"
        },
        {
            "name": "麻腮风疫苗", "code": "MMR", "dose_seq": 1, "type": "FREE", "target_age_month": 8, 
            "description": "预防麻疹、流行性腮腺炎、风疹",
            "side_effects": "接种后6-12天可能出现发热、皮疹（类似轻微麻疹），一般2-3天消退；少数可能出现腮腺肿大。",
            "precautions": "接种后注意观察体温和皮疹情况；发热期间多喝水。",
            "contraindications": "对鸡蛋过敏者慎用；免疫缺陷者、孕妇禁用；急性疾病、发热者暂缓。",
            "interval_info": "基础免疫1剂，加强免疫1剂"
        },
        {
            "name": "乙脑疫苗(减毒)", "code": "JE-L", "dose_seq": 1, "type": "FREE", "target_age_month": 8, 
            "description": "预防流行性乙型脑炎",
            "side_effects": "注射部位红肿、疼痛；少数出现发热、头痛、乏力。",
            "precautions": "接种后观察30分钟；注意休息。",
            "contraindications": "免疫缺陷者禁用；急性疾病、发热者暂缓；过敏体质者慎用。",
            "interval_info": "基础免疫1剂，加强免疫1剂"
        },
        {
            "name": "A群流脑疫苗", "code": "MenA", "dose_seq": 2, "type": "FREE", "target_age_month": 9, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "与A+C群流脑疫苗间隔≥12个月"
        },
        {
            "name": "百白破疫苗", "code": "DTaP", "dose_seq": 4, "type": "FREE", "target_age_month": 18, 
            "description": "第4剂（加强）",
            "side_effects": "加强针局部反应可能较基础免疫重，出现红肿硬结概率较高。",
            "precautions": "同第1剂；注意局部热敷可缓解硬结（接种24小时后）。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "麻腮风疫苗", "code": "MMR", "dose_seq": 2, "type": "FREE", "target_age_month": 18, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "甲肝疫苗(减毒)", "code": "HepA-L", "dose_seq": 1, "type": "FREE", "target_age_month": 18, 
            "description": "预防甲型肝炎",
            "side_effects": "注射部位疼痛、红肿；少数出现低热、乏力。",
            "precautions": "接种后观察30分钟。",
            "contraindications": "免疫缺陷者禁用；急性疾病、发热者暂缓。",
            "interval_info": "仅接种1剂（减毒活疫苗）"
        },
        {
            "name": "乙脑疫苗(减毒)", "code": "JE-L", "dose_seq": 2, "type": "FREE", "target_age_month": 24, 
            "description": "第2剂（加强）",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "A+C群流脑疫苗", "code": "MenAC", "dose_seq": 1, "type": "FREE", "target_age_month": 36, 
            "description": "预防A群、C群流脑",
            "side_effects": "注射部位红肿、疼痛；少数出现发热。",
            "precautions": "接种后观察30分钟。",
            "contraindications": "对疫苗成分过敏者；癫痫、惊厥史者；急性疾病、发热者暂缓。",
            "interval_info": "第1剂与第2剂间隔≥3年"
        },
        {
            "name": "脊灰疫苗(OPV/IPV)", "code": "OPV", "dose_seq": 4, "type": "FREE", "target_age_month": 48, 
            "description": "第4剂，口服", 
            "administration_route": "ORAL",
            "side_effects": "同第3剂。",
            "precautions": "同第3剂。",
            "contraindications": "同第3剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "A+C群流脑疫苗", "code": "MenAC", "dose_seq": 2, "type": "FREE", "target_age_month": 72, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "白破疫苗", "code": "DT", "dose_seq": 1, "type": "FREE", "target_age_month": 72, 
            "description": "预防白喉、破伤风",
            "side_effects": "注射部位红肿、硬结、疼痛；少数出现发热、乏力。",
            "precautions": "接种后观察30分钟。",
            "contraindications": "对疫苗成分过敏者；急性疾病、发热者暂缓。",
            "interval_info": "完成全程接种"
        },
    ]
    
    # 2类自费疫苗（常见）
    paid_vaccines = [
        {
            "name": "五联疫苗", "code": "Pentavalent", "dose_seq": 1, "type": "PAID", "target_age_month": 2,
            "description": "替代脊灰+百白破+Hib，一针预防五种疾病",
            "side_effects": "注射部位红肿、硬结；少数宝宝可能出现发热、烦躁、食欲减退等，症状一般较轻。",
            "precautions": "接种后观察30分钟；注意观察体温；如出现高热、持续哭闹需及时就医；保持接种部位清洁。",
            "contraindications": "对疫苗成分过敏者；有癫痫、惊厥史者；急性疾病、发热者暂缓接种。",
            "interval_info": "基础免疫3剂，各剂间隔≥28天；加强免疫1剂，与第3剂间隔≥6个月"
        },
        {
            "name": "五联疫苗", "code": "Pentavalent", "dose_seq": 2, "type": "PAID", "target_age_month": 3, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "五联疫苗", "code": "Pentavalent", "dose_seq": 3, "type": "PAID", "target_age_month": 4, 
            "description": "第3剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "五联疫苗", "code": "Pentavalent", "dose_seq": 4, "type": "PAID", "target_age_month": 18, 
            "description": "第4剂（加强）",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 1, "type": "PAID", "target_age_month": 2,
            "description": "预防肺炎球菌感染",
            "side_effects": "注射部位红肿、疼痛；部分宝宝可能出现发热、烦躁、食欲减退、嗜睡等。",
            "precautions": "接种后观察30分钟；注意观察体温变化；保持接种部位清洁；如持续发热超过38.5℃需就医。",
            "contraindications": "对疫苗成分过敏者；急性疾病、发热者暂缓接种；有严重心肺疾病者慎用。",
            "interval_info": "基础免疫3剂，各剂间隔≥28天；加强免疫1剂，12-15月龄接种"
        },
        {
            "name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 2, "type": "PAID", "target_age_month": 4, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 3, "type": "PAID", "target_age_month": 6, 
            "description": "第3剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "各剂次间隔≥28天"
        },
        {
            "name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 4, "type": "PAID", "target_age_month": 12, 
            "description": "第4剂（加强）",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "轮状病毒疫苗", "code": "Rota", "dose_seq": 1, "type": "PAID", "target_age_month": 2, 
            "description": "预防轮状病毒肠炎，口服", 
            "administration_route": "ORAL",
            "side_effects": "口服后可能出现轻度腹泻、呕吐、发热、食欲不振。",
            "precautions": "口服前后30分钟避免喂奶、喝热水；注意观察有无肠套叠症状（如剧烈哭闹、果酱样大便）。",
            "contraindications": "有肠套叠史者禁用；胃肠道功能紊乱者慎用；免疫缺陷者禁用。",
            "interval_info": "根据不同品牌（单价/五价），接种剂次和间隔不同，一般间隔4-10周"
        },
        {
            "name": "手足口疫苗(EV71)", "code": "EV71", "dose_seq": 1, "type": "PAID", "target_age_month": 6, 
            "description": "预防EV71病毒引起的手足口病",
            "side_effects": "注射部位红肿、硬结、疼痛；少数出现发热、烦躁、食欲减退。",
            "precautions": "接种后观察30分钟；注意休息。",
            "contraindications": "对疫苗成分过敏者；急性疾病、发热者暂缓。",
            "interval_info": "第1剂与第2剂间隔1个月"
        },
        {
            "name": "手足口疫苗(EV71)", "code": "EV71", "dose_seq": 2, "type": "PAID", "target_age_month": 7, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "水痘疫苗", "code": "Varicella", "dose_seq": 1, "type": "PAID", "target_age_month": 12, 
            "description": "预防水痘",
            "side_effects": "注射部位红肿、疼痛；少数出现发热、皮疹（类似轻微水痘）。",
            "precautions": "接种后观察30分钟；接种后6周内避免接触水杨酸类药物（如阿司匹林）。",
            "contraindications": "免疫缺陷者禁用；急性疾病、发热者暂缓；对新霉素过敏者慎用。",
            "interval_info": "建议接种2剂，间隔≥3个月（部分地区政策不同）"
        },
        {
            "name": "水痘疫苗", "code": "Varicella", "dose_seq": 2, "type": "PAID", "target_age_month": 48, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
        {
            "name": "AC流脑结合疫苗", "code": "MenAC-C", "dose_seq": 1, "type": "PAID", "target_age_month": 6, 
            "description": "替代A群流脑，保护更全面",
            "side_effects": "注射部位红肿、疼痛；少数出现发热。",
            "precautions": "接种后观察30分钟。",
            "contraindications": "对疫苗成分过敏者；急性疾病、发热者暂缓。",
            "interval_info": "根据品牌不同，接种程序略有差异，一般间隔1个月"
        },
        {
            "name": "AC流脑结合疫苗", "code": "MenAC-C", "dose_seq": 2, "type": "PAID", "target_age_month": 7, 
            "description": "第2剂",
            "side_effects": "同第1剂。",
            "precautions": "同第1剂。",
            "contraindications": "同第1剂。",
            "interval_info": "完成全程接种"
        },
    ]
    
    vaccine_crud.init_vaccines(db, free_vaccines + paid_vaccines)
    return {"status": "success", "count": len(free_vaccines) + len(paid_vaccines)}

# === 接种记录 ===

@router.get("/babies/{baby_id}/vaccines", response_model=List[schemas.vaccine.VaccineWithStatus])
def get_baby_vaccines(
    baby_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取宝宝的疫苗接种清单（包含状态）"""
    # 1. 验证权限
    baby = baby_crud.get_baby(db, baby_id)
    if not baby:
        raise HTTPException(status_code=404, detail="宝宝不存在")
    # TODO: 验证用户是否有权访问该宝宝
    
    # 2. 获取所有疫苗
    vaccines = vaccine_crud.get_vaccines(db)
    
    # 3. 获取已接种记录
    records = vaccine_crud.get_baby_vaccination_records(db, baby_id)
    records_map = {r.vaccine_id: r for r in records}
    
    # 4. 计算宝宝当前月龄
    birth_date = baby.birthday
    today = datetime.now().date()
    age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    
    # 6. 统计每个疫苗的总剂数
    vaccine_dose_counts = {}
    for v in vaccines:
        if v.code not in vaccine_dose_counts:
            vaccine_dose_counts[v.code] = 0
        vaccine_dose_counts[v.code] = max(vaccine_dose_counts[v.code], v.dose_seq)
    
    print(f"DEBUG - Vaccine dose counts: {vaccine_dose_counts}")
    
    # 7. 组装结果
    result = []
    for v in vaccines:
        v_dict = v.__dict__.copy()
        record = records_map.get(v.id)
        
        # 添加总剂数
        v_dict['total_doses'] = vaccine_dose_counts.get(v.code, 1)
        
        # 计算预计接种日期
        due_date = birth_date + timedelta(days=v.target_age_month * 30)
        v_dict['due_date'] = due_date.strftime('%Y-%m-%d')
        
        if record:
            v_dict['status'] = record.status
            v_dict['record'] = record
        else:
            # 计算状态
            if v.target_age_month <= age_months:
                # 超过接种月龄1个月未接种，视为超期
                if age_months > v.target_age_month + 1:
                    v_dict['status'] = 'OVERDUE'
                else:
                    v_dict['status'] = 'PENDING' # 到期未接种
            else:
                v_dict['status'] = 'FUTURE' # 未到时间
                
        result.append(v_dict)
        
    return result

@router.get("/babies/{baby_id}/vaccine-config")
def get_vaccine_config(
    baby_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """获取疫苗配置"""
    return vaccine_crud.get_vaccine_config(db, baby_id)

@router.post("/babies/{baby_id}/vaccine-config")
def update_vaccine_config(
    baby_id: int,
    config: Dict[str, Any] = Body(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新疫苗配置"""
    return vaccine_crud.update_vaccine_config(db, baby_id, config)

@router.post("/babies/{baby_id}/vaccines/{vaccine_id}")
def update_vaccination_record(
    baby_id: int,
    vaccine_id: int,
    payload: schemas.vaccine.VaccinationRecordCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新接种记录"""
    # 1. 验证权限
    baby = baby_crud.get_baby(db, baby_id)
    if not baby:
        raise HTTPException(status_code=404, detail="宝宝不存在")
        
    # 2. 更新记录
    record = vaccine_crud.create_or_update_record(
        db, baby_id, vaccine_id,
        status=payload.status,
        vaccination_date=payload.vaccination_date,
        location=payload.location,
        batch_number=payload.batch_number,
        notes=payload.notes,
        photos=payload.photos
    )
    
    return record

@router.delete("/babies/{baby_id}/vaccines/{vaccine_id}")
def delete_vaccination_record(
    baby_id: int,
    vaccine_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除接种记录（重置状态）"""
    vaccine_crud.delete_record(db, baby_id, vaccine_id)
    return {"status": "success"}
