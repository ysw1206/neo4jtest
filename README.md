# Neo4j 테스트 프로젝트

이 예제는 공식 `neo4j` Python 드라이버를 사용하여 모듈과 함수의 간단한 의존성 그래프를 로드하는 방법을 보여줍니다.

## 요구사항

- Python 3.8+
- `neo4j` Python 패키지
- Bolt를 통해 접근 가능한 실행 중인 Neo4j 인스턴스 (예: `bolt://localhost:7687`)

## 설치

의존성을 설치하세요:

```bash
pip install -r requirements.txt
```

또는 직접 설치:

```bash
pip install neo4j
```

## Neo4j 설정

### 1. Neo4j 설치 및 실행

#### Docker를 사용하는 경우:
```bash
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/test \
    -e NEO4J_PLUGINS='["apoc"]' \
    neo4j:latest
```

#### 로컬 설치:
1. [Neo4j Desktop](https://neo4j.com/download/) 또는 [Neo4j Community Edition](https://neo4j.com/download-center/#community) 다운로드
2. Neo4j 서비스 시작
3. 기본 비밀번호를 'test'로 변경

### 2. 환경 변수 설정 (선택사항)

기본값을 변경하려면 환경 변수를 설정하세요:

```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=test
```

## 실행

데이터베이스를 초기화하고, 노드와 관계를 생성한 후, 모듈 `A`와 연결된 노드들을 조회하는 스크립트를 실행하세요:

```bash
python test_neo4j.py
```

## 예상 출력

스크립트 실행 시 다음과 같은 출력을 볼 수 있습니다:

```
Clearing database...
Creating nodes and relationships...
Nodes connected to Module A:
 - B (['Module'])
```

## 프로젝트 구조

이 프로젝트는 다음과 같은 소스코드 구조를 Neo4j 그래프로 표현합니다:

- **모듈 A**는 **모듈 B**를 import
- **모듈 B**는 **함수 foo()**를 포함
- **모듈 C**는 **모듈 A**를 import

### 그래프 구조:
```
(Module A) -[:IMPORTS]-> (Module B) -[:DECLARES]-> (Function foo)
(Module C) -[:IMPORTS]-> (Module A)
```

## Cypher 쿼리 예시

Neo4j 브라우저에서 다음 쿼리들을 실행해볼 수 있습니다:

### 모든 노드 조회:
```cypher
MATCH (n) RETURN n
```

### 모듈 A와 연결된 모든 노드:
```cypher
MATCH (a:Module {name: 'A'})--(n) 
RETURN n.name as name, labels(n) as labels
```

### 모든 import 관계 조회:
```cypher
MATCH (a)-[r:IMPORTS]->(b) 
RETURN a.name, b.name
```

### 모든 함수 선언 관계 조회:
```cypher
MATCH (m)-[r:DECLARES]->(f) 
RETURN m.name, f.name
```
