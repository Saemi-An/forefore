# ============================ 스타일 ============================

# 커밋 전에 pre-commit 툴을 사용하여 코드 스타일 수동 확인
.PHONY: lint
lint:
	poetry run pre-commit run --all-files


# hook에 변경사항이 있을 때 pre-commit 도구를 통해 기존 hook 전체 삭제 및 재다운로드
.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

# ============================ 장고 ============================

# 개발서버 DB 컨테이너 띄우기 
.PHONY: up-dependencies-only
up-dependencies-only:
	docker-compose -f docker-compose.dev.yml up --force-recreate db

# 개발서버 실행
.PHONY: run
run:
	poetry run python -m core.manage runserver

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: create_superuser
create_superuser:
	poetry run python -m core.manage createsuperuser

# ============================ 초기 설정 ============================

# .toml 파일 기반으로 의존성 패키지 설치
.PHONY: install
install:
	poetry install

# 프로젝트 최신 상태로 셋업
.PHONY: update
update: install migrate install-pre-commit ;