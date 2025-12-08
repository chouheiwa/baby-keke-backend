from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.album import AlbumRecordCreate, AlbumRecordResponse
from wxcloudrun.crud import album as album_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/album",
    tags=["成长相册"]
)

@router.post("/", response_model=AlbumRecordResponse, status_code=status.HTTP_201_CREATED)
def create_album_record(
    record: AlbumRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建相册记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = album_crud.create_album_record(db, record, user_id)
    return AlbumRecordResponse.model_validate(created, from_attributes=True)

@router.get("/baby/{baby_id}", response_model=List[AlbumRecordResponse])
async def get_album_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数")
):
    """获取宝宝的相册记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = album_crud.get_album_records_by_baby(db, baby_id, skip, limit)
    
    # 获取临时链接
    if records:
        from wxcloudrun.utils.wechat import get_wechat_api
        wx_api = get_wechat_api()
        
        file_list = [{"fileid": r.file_id, "max_age": 7200} for r in records]
        try:
            download_list = await wx_api.batch_download_file(file_list)
            # 构建 file_id -> url 的映射
            url_map = {item["fileid"]: item["temp_file_url"] for item in download_list if item["status"] == 0}
        except Exception as e:
            print(f"Failed to get signed urls: {e}")
            url_map = {}
            
        # 组装结果
        results = []
        for r in records:
            resp = AlbumRecordResponse.model_validate(r, from_attributes=True)
            resp.url = url_map.get(r.file_id)
            results.append(resp)
        return results
        
    return []

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除相册记录"""
    db_record = album_crud.get_album_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    
    verify_baby_access(db_record.baby_id, user_id, db)
    
    # TODO: 理想情况下应该先删除云存储文件，但后端没有云存储SDK，
    # 且前端可以直接删除，或者后端只负责删除元数据，文件由生命周期管理或定期清理
    
    success = album_crud.delete_album_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None
