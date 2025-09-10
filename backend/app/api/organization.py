from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.organization import OrganizationCreate, OrganizationOut, OrganizationUpdate
from app.models.organization import Organization
from app.dependencies import get_db

router = APIRouter()

@router.post("/organizations", response_model=OrganizationOut)
def create_organization(data: OrganizationCreate, db: Session = Depends(get_db)):
    existing = db.query(Organization).filter(Organization.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Такая организация уже существует")
    org = Organization(name=data.name, description=data.description)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.put("/organizations/{org_id}", response_model=OrganizationOut)
def update_organization(org_id: int, data: OrganizationUpdate, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    
    org.name = data.name
    org.description = data.description
    db.commit()
    db.refresh(org)
    return org

@router.delete("/organizations/{org_id}")
def delete_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    db.delete(org)
    db.commit()
    return {"detail": "Организация удалена"}


@router.get("/organizations", response_model=list[OrganizationOut])
def get_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()

@router.get("/organizations/{org_id}", response_model=OrganizationOut)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org
