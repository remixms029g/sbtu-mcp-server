# วิธีการมีส่วนร่วมในโปรเจกต์ (Contributing Guide)

ขอบคุณที่สนใจมีส่วนร่วมในโปรเจกต์ SBTU MCP Server! 🙏

## ขั้นตอนการมีส่วนร่วม

### 1. Fork Repository
ไปที่ [GitHub Repository](https://github.com/remixms029g/sbtu-mcp-server) และคลิก "Fork"

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR-USERNAME/sbtu-mcp-server.git
cd sbtu-mcp-server
```

### 3. Create Feature Branch
```bash
# สร้าง branch ใหม่จาก develop
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- แก้ไขโค้ดตามที่ต้องการ
- เพิ่ม tests สำหรับการเปลี่ยนแปลง
- อัปเดต documentation ถ้าจำเป็น

### 5. Run Tests Locally
```bash
pip install -e .
pip install pytest pytest-cov flake8 black isort
pytest src/ -v
flake8 src/
black src/
isort src/
```

### 6. Commit Changes
```bash
git add .
git commit -m "feat: คำอธิบายว่าเปลี่ยนแปลงอะไร"
```

### 7. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 8. Create Pull Request
- ไปที่ GitHub repository
- คลิก "Compare & pull request"
- เขียนรายละเอียด PR ให้ชัดเจน
- คลิก "Create pull request"

## Commit Message Convention

เราใช้ Conventional Commits:

```
feat: เพิ่มฟีเจอร์ใหม่
fix: แก้ไข bug
docs: อัปเดต documentation
style: การเปลี่ยนแปลง formatting
refactor: โครงสร้างโค้ดใหม่โดยไม่เปลี่ยน functionality
test: เพิ่ม tests
chore: อัปเดต dependencies
```

### ตัวอย่าง
```
feat: เพิ่ม GitHub issue management
fix: แก้ไข token validation error
docs: อัปเดต installation guide
```

## Branch Strategy

### Main Branches
- **main** - Production ready code
- **develop** - Development branch

### Feature Branches
```
feature/feature-name
bugfix/bug-name
hotfix/issue-name
docs/documentation-name
```

## Code Style Guidelines

### Python Code Style
- ใช้ PEP 8
- ใช้ Black สำหรับ formatting
- ใช้ isort สำหรับ import sorting
- ใช้ type hints ที่เป็นไปได้

### Example
```python
from typing import Optional, Dict, List

def create_pull_request(
    repo: str,
    title: str,
    body: Optional[str] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, str]:
    """สร้าง pull request ใน GitHub
    
    Args:
        repo: Repository name
        title: PR title
        body: PR description
        labels: List of labels
        
    Returns:
        PR details dictionary
    """
    pass
```

## Testing Requirements

- เขียน tests สำหรับทุก feature ใหม่
- ทำให้ test coverage อย่างน้อย 80%
- ตรวจสอบว่า tests ผ่านทั้งหมดก่อน submit PR

```bash
pytest src/ -v --cov=src/ --cov-report=term-missing
```

## Documentation

- อัปเดต README.md ถ้าเพิ่ม features ใหม่
- เพิ่ม docstrings ใน functions และ classes
- เพิ่ม comments ในโค้ดที่ซับซ้อน

## Pull Request Process

1. อัปเดต DEVELOPMENT_LOG.md ด้วยการเปลี่ยนแปลงของคุณ
2. ตรวจสอบว่า CI/CD tests ผ่านทั้งหมด
3. อย่างน้อย 1 reviewer ต้อง approve
4. ลบ feature branch หลังจากรวม

## Report Issues

หากพบ bug:

1. ไปที่ [Issues page](https://github.com/remixms029g/sbtu-mcp-server/issues)
2. คลิก "New issue"
3. เขียนรายละเอียด:
   - ชื่อปัญหา
   - ขั้นตอนการทำให้เกิด bug
   - พฤติกรรมที่คาดหวัง
   - พฤติกรรมจริง
   - Environment (OS, Python version)

## Questions?

ถ้ามีคำถามเก็บไว้ใน [GitHub Discussions](https://github.com/remixms029g/sbtu-mcp-server/discussions)

## Code of Conduct

- เคารพและเป็นมิตรต่อเพื่อนร่วมงาน
- ห้ามใช้ภาษาหยาบคาย
- ยอมรับ feedback ที่สร้างสรรค์
