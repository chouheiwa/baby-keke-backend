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
    free_vaccines = [
        {"name": "乙肝疫苗", "code": "HepB", "dose_seq": 1, "type": "FREE", "target_age_month": 0, "description": "出生后24小时内接种"},
        {"name": "卡介苗", "code": "BCG", "dose_seq": 1, "type": "FREE", "target_age_month": 0, "description": "出生时接种"},
        {"name": "乙肝疫苗", "code": "HepB", "dose_seq": 2, "type": "FREE", "target_age_month": 1, "description": ""},
        {"name": "脊灰疫苗(IPV)", "code": "IPV", "dose_seq": 1, "type": "FREE", "target_age_month": 2, "description": ""},
        {"name": "脊灰疫苗(IPV)", "code": "IPV", "dose_seq": 2, "type": "FREE", "target_age_month": 3, "description": ""},
        {"name": "百白破疫苗", "code": "DTaP", "dose_seq": 1, "type": "FREE", "target_age_month": 3, "description": ""},
        {"name": "脊灰疫苗(OPV/IPV)", "code": "OPV", "dose_seq": 3, "type": "FREE", "target_age_month": 4, "description": ""},
        {"name": "百白破疫苗", "code": "DTaP", "dose_seq": 2, "type": "FREE", "target_age_month": 4, "description": ""},
        {"name": "百白破疫苗", "code": "DTaP", "dose_seq": 3, "type": "FREE", "target_age_month": 5, "description": ""},
        {"name": "乙肝疫苗", "code": "HepB", "dose_seq": 3, "type": "FREE", "target_age_month": 6, "description": ""},
        {"name": "A群流脑疫苗", "code": "MenA", "dose_seq": 1, "type": "FREE", "target_age_month": 6, "description": ""},
        {"name": "麻腮风疫苗", "code": "MMR", "dose_seq": 1, "type": "FREE", "target_age_month": 8, "description": ""},
        {"name": "乙脑疫苗(减毒)", "code": "JE-L", "dose_seq": 1, "type": "FREE", "target_age_month": 8, "description": ""},
        {"name": "A群流脑疫苗", "code": "MenA", "dose_seq": 2, "type": "FREE", "target_age_month": 9, "description": ""},
        {"name": "百白破疫苗", "code": "DTaP", "dose_seq": 4, "type": "FREE", "target_age_month": 18, "description": ""},
        {"name": "麻腮风疫苗", "code": "MMR", "dose_seq": 2, "type": "FREE", "target_age_month": 18, "description": ""},
        {"name": "甲肝疫苗(减毒)", "code": "HepA-L", "dose_seq": 1, "type": "FREE", "target_age_month": 18, "description": ""},
        {"name": "乙脑疫苗(减毒)", "code": "JE-L", "dose_seq": 2, "type": "FREE", "target_age_month": 24, "description": ""},
        {"name": "A+C群流脑疫苗", "code": "MenAC", "dose_seq": 1, "type": "FREE", "target_age_month": 36, "description": ""},
        {"name": "脊灰疫苗(OPV/IPV)", "code": "OPV", "dose_seq": 4, "type": "FREE", "target_age_month": 48, "description": ""},
        {"name": "A+C群流脑疫苗", "code": "MenAC", "dose_seq": 2, "type": "FREE", "target_age_month": 72, "description": ""},
        {"name": "白破疫苗", "code": "DT", "dose_seq": 1, "type": "FREE", "target_age_month": 72, "description": ""},
    ]
    
    # 2类自费疫苗（常见）
    paid_vaccines = [
        {"name": "五联疫苗", "code": "Pentavalent", "dose_seq": 1, "type": "PAID", "target_age_month": 2, "description": "替代脊灰+百白破+Hib"},
        {"name": "五联疫苗", "code": "Pentavalent", "dose_seq": 2, "type": "PAID", "target_age_month": 3, "description": ""},
        {"name": "五联疫苗", "code": "Pentavalent", "dose_seq": 3, "type": "PAID", "target_age_month": 4, "description": ""},
        {"name": "五联疫苗", "code": "Pentavalent", "dose_seq": 4, "type": "PAID", "target_age_month": 18, "description": ""},
        {"name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 1, "type": "PAID", "target_age_month": 2, "description": ""},
        {"name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 2, "type": "PAID", "target_age_month": 4, "description": ""},
        {"name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 3, "type": "PAID", "target_age_month": 6, "description": ""},
        {"name": "13价肺炎疫苗", "code": "PCV13", "dose_seq": 4, "type": "PAID", "target_age_month": 12, "description": "12-15月龄"},
        {"name": "轮状病毒疫苗", "code": "Rota", "dose_seq": 1, "type": "PAID", "target_age_month": 2, "description": ""},
        {"name": "手足口疫苗(EV71)", "code": "EV71", "dose_seq": 1, "type": "PAID", "target_age_month": 6, "description": ""},
        {"name": "手足口疫苗(EV71)", "code": "EV71", "dose_seq": 2, "type": "PAID", "target_age_month": 7, "description": "间隔1个月"},
        {"name": "水痘疫苗", "code": "Varicella", "dose_seq": 1, "type": "PAID", "target_age_month": 12, "description": ""},
        {"name": "水痘疫苗", "code": "Varicella", "dose_seq": 2, "type": "PAID", "target_age_month": 48, "description": ""},
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
    birth_date = baby.birth_date
    today = datetime.now().date()
    age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
    
    # 5. 组装结果
    result = []
    for v in vaccines:
        v_dict = v.__dict__.copy()
        record = records_map.get(v.id)
        
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
