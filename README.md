# ICML 연구실 웹사이트

Intelligent Control & Machine Learning Lab, Incheon National University.

기존 al-folio를 제거하고 보존한 연구실 자료를 Academic Pages의 학술 사이트 구조에 연결한 Jekyll 사이트입니다. 2026-10-26 사용자가 Academic Pages 적용과 Jekyll 사용을 승인했습니다. 검토 후 사용자가 사진 추가와 홈페이지 배포를 요청했습니다. 공개 주소는 https://mhlee-icml.github.io/ 입니다.

## 현재 사이트와 실행

Academic Pages의 상단 메뉴·왼쪽 소개·오른쪽 본문 구조를 연구실용으로 재구성했습니다. 로고, 연구 분야, 뉴스, 연구 영상과 대표 논문을 홈에 배치하고 Research, Publications, Projects, People, News, Videos, Join Us 및 Professor·Alumni 상세 페이지를 제공합니다. 논문 페이지에는 전체 목록 검색이 있습니다. 데모 인물·논문·과제는 가져오지 않았습니다.

기술 구성은 **Jekyll 4.4 / Liquid / HTML / CSS / JavaScript**입니다. Python 3.10 이상(추가 패키지 없음)이 `content/`를 읽어 `_data/lab.json`과 `_pages/`를 생성하며, Jekyll이 `_site/`를 빌드합니다. 원문을 수정하지 않고 교수 이력과 연구 소개 전체를 렌더링합니다. 출처와 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에 있습니다.

이 PC에는 저장소 내부 `.tools/`에 로컬 Ruby와 빌드 라이브러리를 준비했습니다. 시스템 전체에 설치하지 않았으며 Git에도 포함되지 않습니다. 이 작업 폴더에서는 다음 명령으로 빌드·검증·미리보기를 실행합니다.

```powershell
python scripts/site.py preview
```

미리보기 주소는 `http://127.0.0.1:8765/`입니다. 종료는 `Ctrl+C`, 포트 변경은 `--port 8766`입니다. 실행 중 수정 사항을 반영하려면 별도 터미널에서 `python scripts/site.py build`를 실행한 뒤 브라우저를 새로고침합니다. 이 PC에서는 4000 포트의 사용이 제한되어 8765를 기본값으로 정했습니다.

```powershell
python scripts/site.py build              # 데이터 생성 → Jekyll 빌드 → 보존·링크 검사
python scripts/site.py serve              # 이미 생성한 _site/만 로컬에서 제공
python scripts/validate.py --require-build
```

슬라이드 동작 검증은 Node.js가 있는 환경에서 `node scripts/test_carousel.mjs`로 실행합니다. 추가 패키지 없이 자동 전환·버튼·스와이프·일시정지·접근성 상태를 검사하는 DOM/타이머 모의 테스트이며 실제 브라우저 화면 검증은 아닙니다. Node.js는 사이트 빌드나 미리보기 실행에는 필요하지 않습니다.

새 PC에서는 Python 3.10 이상, Ruby/Bundler(Windows는 Ruby+Devkit)를 준비한 뒤 아래 명령을 실행합니다.

```text
bundle install
python scripts/site.py preview
```

표준 Jekyll 명령을 직접 실행할 수도 있습니다.

```text
python scripts/prepare.py
bundle exec jekyll build
python scripts/validate.py --require-build
python scripts/site.py serve
```

로컬 Windows용 `scripts/build_jekyll.rb`는 같은 Jekyll 엔진으로 정적 빌드를 수행하고, 개발 서버의 네이티브 live-reload 의존성만 사용하지 않습니다. 미리보기 서버는 Python이며 자동 새로고침은 없습니다.

첫 시안은 이 로컬 빌드 경로로 검증했습니다. 전체 `bundle install`은 이 PC에서 완료하지 않았으며, 표준 설치에는 Ruby+Devkit 등 해당 플랫폼의 빌드 도구가 필요합니다. 현재 자동 검증은 원문·이미지 보존, 내부 링크 및 HTTP 응답을 포함합니다. 브라우저 자동 제어 연결을 사용할 수 없어 화면 캡처와 실제 브라우저 상호작용 검증은 수행하지 못했습니다.

GitHub Pages 배포는 `.github/workflows/pages.yml`이 담당합니다. `main` 푸시 또는 Actions의 **Build and deploy ICML site → Run workflow**로 실행합니다. Ubuntu에서 Python 3.13, Ruby 3.3, Node.js 24를 준비하고 잠긴 Ruby 의존성을 설치한 뒤, 데이터 생성 → 슬라이드 동작 검사 → Jekyll production 빌드 → 콘텐츠·이미지·내부 링크 검사 → `_site/` 업로드 → 배포 순서로 진행합니다. 검사가 실패하면 배포하지 않으며 배포 작업은 `main`에서만 실행됩니다.

저장소 **Settings → Pages → Build and deployment → Source**는 **GitHub Actions**를 사용해야 합니다. `github-pages` 환경의 배포 규칙도 `main`을 허용해야 합니다. 게시 완료 여부는 Actions의 배포 성공과 공개 페이지 응답으로 확인합니다. 로컬 도구·캐시·생성 파일은 Git에 포함하지 않습니다. 이후 커밋·푸시·배포도 사용자의 요청 범위에서 진행합니다.

## 수정 위치와 검증

- 원문·연결: `content/`, 이미지 원본: `assets/img/`
- 홈 슬라이드: `content/platforms.json`에서 순서·사진·설명·핵심 기술 또는 연구 분야·영상 이동 링크를 수정합니다. `source_details`와 `source_notes`는 출처 보존용이며 화면에 표시하지 않습니다.
- 화면 구성: `_layouts/`, 공통 메뉴·사이드바·푸터: `_includes/`
- 메뉴: `_data/navigation.yml`, 스타일: `assets/css/lab.css`, 동작: `assets/js/lab.js`
- 프로필 사진: 교수·학생·졸업생과 사진 없는 자리 모두 데스크톱 180×225px, 600px 이하 화면 120×150px로 통일합니다. 교수 상세 페이지도 같은 규격을 사용하며 사진 원본은 수정하지 않습니다.
- 자동 생성물: `_data/lab.json`, `_pages/`, `_site/` — 직접 수정하지 않습니다.
- 검사: 원본 파일 해시, 논문 30개와 대표 논문 6개, 연구 이미지 10개, 구성원·영상·뉴스 연결, 생성된 페이지의 내부 링크와 앵커, 본문·이미지 보존을 확인합니다.

`.cache/icml-content-baseline.json`은 첫 빌드의 로컬 보존 기준입니다. 사용자가 원문 수정을 승인한 경우 변경 내용을 검토한 뒤 해당 로컬 기준을 갱신해야 합니다. `content/inventory.json`은 별도의 과거 보존 기록이며 현재 자료를 덮어쓰는 기준이 아닙니다.

## 보존한 자료

| 위치 | 내용 |
| --- | --- |
| [content/site.json](content/site.json) | 연구실 이름, 사이트 주소, 연락처, 기존 메뉴·경로, 홈 이미지 연결 |
| [content/pages/professor.md](content/pages/professor.md) | 교수 소개, 학력·경력·강의·과제·논문·특허·학술활동·수상 원문 |
| [content/pages/research-fields.md](content/pages/research-fields.md) | 연구 분야 3개, 설명과 연구 이미지 10개의 연결 |
| [content/pages/join-us.md](content/pages/join-us.md) | 대학원 진학·학부연구 참여 모집과 연구실 홍보, 교수 이메일 문의 안내 |
| [content/people.json](content/people.json) | 현재 대학원생 1명·학부연구생 3명과 졸업생 1명의 이름·소속·사진·소개 연결 |
| [content/people/](content/people/) | 김형진·김예훈·길순형·장윤서 소개 각 1개와 졸업생 소개 1개 |
| [content/news/](content/news/) | KAIST Mobility Challenge 대상 브릿지경제 보도와 RoboCup 2026 SML 우승 중앙일보 보도 |
| [content/videos.json](content/videos.json) | 연구 영상 3개의 YouTube 주소·제목·캡션 |
| [content/platforms.json](content/platforms.json) | 홈 연구 플랫폼 5개의 사진·설명·기술 또는 연구 분야·영상 이동 링크와 제공 원문·근거 |
| [assets/img/](assets/img/) | 연구실 사진·로고·연구 도표·포스터 원본 28개 |
| [content/inventory.json](content/inventory.json) | 원본·새 경로, SHA-256, 제거 분류와 확인 사항 |

기존 이미지 17개는 이름·경로·파일 내용이 원본과 동일합니다. 새로 제공된 `yh_kim.jpg`, `ys_jang.jpg`, `sh_kil.png`, 연구 사진 5개, RoboCup 우승 사진 1개와 새 로고 2개는 파일 내용을 변경하지 않고 `assets/img/`로 옮겨 현재 이미지가 28개입니다. 기존 연구실 로고 `icmllogo.png`, 행사 사진 `kaistimg.png`, 한국어 연구 포스터 `labhomepage.png`도 원본 그대로 보존합니다. 시현의 소개 원본 1개를 유지하고, 사용자가 삭제한 우진·다인·기현의 소개와 사진은 구성원 목록에서도 제외했습니다.

사이드바에는 사용자가 최종 선택한 네이비 배경 가로형 로고 `icml-logo-wide-dark.png`를 사용합니다. 원래 파일명은 `네이비 배경의 ICML LAB 로봇 로고.png`이며 1774×887 원본을 이름만 바꿔 저장했습니다. 앞서 저장한 흰색 정사각형 로고 `icml-logo-square-light.png`(원래 파일명 `중앙 정렬 ICML LAB 로봇 로고-3.png`, 1254×1254)도 유지하여 새 로고 원본은 총 2개입니다. 기존 `icmllogo.png` 역시 덮어쓰지 않습니다. 현재 표시에는 최종 선택을 적용하고 이전 선택·저장 요청은 `content/inventory.json`의 과거 기록으로 보존합니다.

새 연구 사진 `erp42-autonomous-driving.webp`, `robocup-sml-mobile-manipulator.webp`, `smart-stroller.webp`는 홈 상단 슬라이드에 사용합니다. 홈의 **Research in motion** 영역은 `content/videos.json`에 등록된 영상 중 앞의 3개를 같은 크기의 16:9 YouTube 플레이어로 보여줍니다. 현재는 KAIST 협력 자율주행, AMR·매니퓰레이터, ERP42 자율주행 영상이며 원래 제목·캡션·주소를 유지합니다. 화면 폭에 따라 3열·2열·1열로 배치되고, 홈에서 직접 재생하거나 YouTube 및 전체 영상 페이지로 이동할 수 있습니다. 사용자 제공 우승 사진 `인천대_TEAM_INU_로보컵_2026_SML_부문_세계_1위.png`는 `robocup-2026-sml-champions.png`로 이름만 바꿔 RoboCup 뉴스에 연결했습니다. 뉴스 날짜·제목·본문·출처와 기존 영상 주소·캡션은 유지하며, 새 이미지의 원래 이름과 SHA-256은 `content/inventory.json`의 후속 기록에 보존합니다.

로봇개 사진 `KakaoTalk_20261026_153913472.jpg`와 드론 실험 플랫폼 사진 `KakaoTalk_20261026_153919475.jpg`는 각각 `quadruped-robot.jpg`, `drone-platform.jpg`로 이름만 바꿔 홈 상단 슬라이드에 추가했습니다. 원본 이미지의 파일 내용과 해상도는 유지하며 제조사·모델명은 추정하지 않습니다.

홈 상단은 ERP-42 → Mobile Manipulator → Smart Stroller → Quadruped Robot → Drone Platform 순서의 5개 항목으로, 사진과 설명이 함께 옆으로 넘어가는 슬라이드입니다. 5초마다 자동 전환하며 이전·다음 버튼, 선택 점, 키보드 방향키, 모바일 스와이프와 재생·일시정지를 지원합니다. 마우스를 올리거나 키보드 포커스가 들어오면 자동 전환을 멈추고, 화면 밖이나 숨겨진 탭에서는 타이머를 쉬게 합니다. 움직임 줄이기 설정에서는 자동 재생을 시작하지 않으며, JavaScript가 없어도 다섯 항목의 사진과 설명을 모두 볼 수 있습니다. 내용은 `content/platforms.json`, 구성은 `_layouts/home.html`, 표시와 동작은 `assets/css/lab.css` 및 `assets/js/lab.js`에서 수정합니다.

모든 슬라이드에 영상 이동 링크를 제공합니다. ERP-42는 해당 영상(`/videos/#video-3`), Mobile Manipulator는 관련 영상(`/videos/#video-2`)으로 이동합니다. 전용 영상이 없는 Smart Stroller·Quadruped Robot·Drone Platform은 사용자 요청에 따라 전체 영상 페이지(`/videos/`)로 이동하며 **Browse research videos**로 표시합니다. 없는 영상을 새로 등록하거나 특정 플랫폼의 영상으로 오인하게 연결하지 않습니다.

ERP-42와 Smart Stroller의 두 문장 설명과 **Core technology**는 사용자가 제공한 내용을 반영했고, 제공 원문 전체는 `content/platforms.json`의 `source_details`에 보존합니다. 다른 플랫폼의 **Research focus**는 기존 연구 소개·관련 영상·제공 사진을 근거로 합니다. 드론의 관련 UAV 연구 설명은 사진 속 실험 장치에 특정 논문 알고리즘을 적용했다는 주장이 아니며, 세부 근거는 `source_notes`에 기록합니다.

교수·연구 소개는 글과 의미 있는 HTML 구조를 유지하면서 테마의 CSS, 클래스, Liquid 표현식과 표시 설정을 제거했습니다. 이미지 경로와 대체 텍스트, 이메일 링크, 모든 문구와 목록 순서를 보존했습니다. 홈 본문은 원래 비어 있었으며 연구실 전체 명칭과 홈 이미지 연결은 `site.json`에 있습니다.

김형진 / Hyeongjin Kim은 **Graduate students** 구역의 **Integrated M.S.–Ph.D. Student**로 표시합니다. 소속은 **Hanyang University · Department of Electrical Engineering**, 공개 이메일은 `ky942400@hanyang.ac.kr`, 연구 관심분야는 Reinforcement Learning / Intelligent Manipulation / Intelligent Robotics입니다. 소개 원본은 `content/people/about_hj_kim.md`이며 제공된 사진이 없어 다른 프로필과 같은 크기의 자리표시자를 사용합니다. 대학원생 구역은 교수 소개 다음, 학부연구생 구역 앞에 배치합니다.

사용자 확인에 따라 학부연구생은 **김예훈 → 길순형 → 장윤서** 순서의 현재 참여 구성원(`status: current`)입니다. 김예훈·길순형은 전기공학과(Department of Electrical Engineering), 장윤서는 임베디드 시스템 공학과(Department of Embedded Systems Engineering)로 표시합니다. 김예훈은 `yh_kim.jpg`와 `content/people/about_yh_kim.md`를 연결했습니다. 장윤서는 `ys_jang.jpg`와 `content/people/about_ys_jang.md`에 이메일 `jyoonseo45@gmail.com`, 관심분야 Robot Control / Robot Manipulators / Robot Path Planning을 연결했습니다. 길순형은 `content/people/about_sh_kil.md`에 이메일 `kilsh1210@inu.ac.kr`, 관심분야 Drone Swarm Control / Reinforcement Learning을 연결했습니다. 길순형의 사진은 사용자 제공 파일 `자연스러운 고해상도 인물 사진 복원.png`를 원본 내용 그대로 `sh_kil.png`로 정리해 연결했습니다. 다른 구성원과 같은 크기와 4:5 표시 비율을 사용합니다. 모든 프로필 이메일은 클릭 가능한 메일 링크입니다. 졸업생의 기존 연결은 유지합니다.

Join Us는 **대학원 진학(석사·박사과정)과 학부연구 참여**를 함께 안내하는 한국어 모집·홍보 페이지입니다. 연구 분야, 실제 로봇 사진, 연구 영상·논문·구성원 링크, 교수님 이메일 `mh.lee@inu.ac.kr` 문의 버튼을 제공합니다. 자기소개·관심 분야·진학 또는 참여 희망 시기는 문의 시 참고 안내이며 별도 성적 기준, 모집 마감일, 지원금이나 합류 일정을 임의로 정하지 않았습니다. 모집 안내는 `content/pages/join-us.md`에서 수정합니다.

## 뉴스 작성 형식

모든 뉴스는 `content/news/YYYY-MM-DD-slug.md`에 저장하고 다음 항목을 같은 순서로 작성합니다.

`title`, `date`, `image`, `source`, `source_title`, `source_url`, `source_date`, `date_source_url`

- `title`: 팀 이름과 성과를 담은 영어 제목. 원문 제목은 `source_title`에 원문 언어로 보존합니다.
- `date`: 뉴스의 기준 날짜. 기존 뉴스 날짜를 우선하고, 신규 보도만 있는 경우 확인된 기사 날짜를 사용합니다.
- `source_date`: 기사 발행 날짜. `date`와 함께 `YYYY-MM-DD`로 표기합니다.
- `image`: 기존 로컬 이미지 경로. 사용할 이미지가 없으면 `null`로 둡니다.
- `source`: 원문 매체명, `source_url`: 원문 기사 URL, `date_source_url`: 기사 날짜를 확인한 URL.
- 본문은 영어 요약 두 문단(성과·대회 정보 → 연구실·지도교수·참여자 관련 내용) 뒤 원문 링크 한 줄로 통일합니다.
- 원문 링크는 `[Read the coverage in 매체 영문명 (Korean)](원문 URL).` 형식으로 작성합니다.
- 형식을 맞출 때 기존 사실·날짜·참가자 정보와 사진은 보존합니다.

## 분석 결과

실제 논문은 기존 `_pages/professor.md`에 있었습니다. 전체 목록 30개와 대표 논문 표시 6개를 그대로 보존했습니다. 전체 목록은 국제학술지 게재·승인 9개, 심사 중 2개, Top AI Conferences 1개, 국제학회 10개, 국내학술지 2개, 국내학회 6개입니다. 대표 논문은 전체 목록과 중복되므로 36편으로 세지 않습니다.

같은 파일의 연구 과제 14개, 강의 이력 9개 학기 행, 특허 출원 3개, 심사 학술지 9개, 초청 강연 4개, 수상 4개도 보존했습니다.

기존 `_bibliography/papers.bib`는 Einstein 예제 3개였고 `_projects/`의 3개 항목도 테마 데모였습니다. `_data/`의 CV·연락처·공저자 정보, 블로그 31개, 예제 강의·도서·PDF·영상 역시 연구실 자료가 아니어서 제거했습니다. 프로젝트와 논문 페이지의 기존 경로·분류명은 `site.json`에 남아 있습니다.

Jekyll/Liquid 템플릿, 스타일·스크립트·폰트, Ruby/Node 의존성, Docker 설정, GitHub Actions, 테마 설명서와 미리보기도 제거했습니다. 기존 테마의 출처 기록으로 [LICENSE](LICENSE)를 보존했습니다.

## 원문대로 남긴 확인 사항

- KAIST 대회의 공식 명칭에는 2025년이 포함되지만 수상자 발표는 2026-02-10입니다. [브릿지경제 기사](https://www.viva100.com/article/20260212501397)로 확인했습니다. 뉴스 날짜는 2026-02-10, 기사 발행일인 `source_date`는 2026-02-12로 구분하고 기존 사진을 유지했습니다.
- 교수 주소는 `Room #251, Building 8`, 공통 연락처는 `Room 251, Bldg 8-B`로 서로 다릅니다.
- 논문 심사 상태, 과제 기간, 재직·학위 정보는 기존 원문 기준이며 현재 상태로 갱신하지 않았습니다.

## 보존 검증과 후속 작업

정리 전 기준 커밋은 `3bbc154ef9835c5c67253086c605d54a236875b2`입니다. 원본 파일은 이 커밋의 Git 이력에서도 확인할 수 있습니다. 이번 정리에서는 커밋이나 원격 배포를 수행하지 않았습니다.

최초 정리 시점에는 이미지 20개와 소개 원본 4개의 SHA-256, 교수·연구 본문, 이미지·링크와 JSON 연결을 검사했습니다. `content/inventory.json`의 `retained`, `migrated`, `outputs`는 그 시점의 기록이며 현재 파일 목록이 아닙니다. 이후 사용자 삭제와 뉴스 형식 변경은 `follow_up_changes`에 기록했습니다. 현재 구성원과 뉴스는 각각 `content/people.json`과 `content/news/`를 기준으로 사용합니다.

현재 사이트는 `content/`와 `assets/img/`를 입력으로 사용합니다. JSON의 파일 경로는 저장소 루트 기준이며 `/assets/...`는 사이트 루트 기준입니다. `site.json`의 기존 페이지 경로를 유지했습니다. 앞의 보존 기록은 al-folio 정리 당시의 작업 내역이며, 현재 실행 방식은 이 README의 「현재 사이트와 실행」을 기준으로 합니다.
