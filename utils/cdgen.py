import requests
import utils.config as config

API_URL = None
def init_cdgen():
    global API_URL
    API_URL = config.get_option("apis.kcd_api")

init_cdgen()

def generate(query):
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url=API_URL, headers=headers,json={"query": query} )
        response.raise_for_status()

        # 응답 데이터 출력
        print("응답 코드:", response.status_code)
        print("응답 본문:", response.json())
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        print("응답 코드:", response.status_code)
        print("응답 본문:", response.text)

    except requests.exceptions.ConnectionError:
        print("연결 오류 발생. 서버에 접근할 수 없습니다.")

    except requests.exceptions.Timeout:
        print("요청 시간이 초과되었습니다.")

    except requests.exceptions.RequestException as err:
        print(f"알 수 없는 오류 발생: {err}")

    return None

if __name__ == "__main__":
    medical_record = """주요 증상:\n코 비틀어짐으로 인한 호흡 곤란\n수년 전 코 부딪힘 이후 증상 발생\n수면 시 한쪽 코 막힘, 입 호흡\n아침 기상 시 목 통증, 피로감\n\n
    진찰 소견:\n비중격 만곡증 의심\n\n
    진단:\n3D CT 촬영 예정\n\n
    치료 계획:\n비중격 만곡증 수술\n휘어진 비중격 연골 교정\n코 성형 수술 (환자 희망)\n낮은 콧대, 뭉툭한 코끝 개선\n환자 얼굴 고려, 자연스러운 코 라인 목표\n
    수술 방법: 전신 마취, 약 2시간 소요\n
    입원 치료: 1-2일 예상\n
    일상생활 복귀: 약 1주일 후\n
    완전 회복: 6개월-1년\n\n
    수술 전 주의사항:\n수술 2주 전부터 금연, 금주\n아스피린, 비타민 E 등 약물 복용 중단\n\n
    향후 계획:\n3D CT 촬영 결과 토대로 수술 계획 수립 및 상담 예정
    """

    response = generate(medical_record)
    print(dir(response))
    print(response, end="\t")

'''
[
    {
        "code": "R06.0",
        "description": "Dyspnea",
        "subCodes": [
            {
                "code": "R06.0",
                "description": "호흡곤란\r\n Dyspnea",
                "relevance_score": 0.4
            },
            {
                "code": "G62.0",
                "description": "약물의 분류를 원한다면 부가적인 외인분류코드(XX장)를 사용할 것.",
                "relevance_score": 0.1
            },
            {
                "code": "J38.40",
                "description": "라인케부종",
                "relevance_score": 0.2
            },
            {
                "code": "U07.0",
                "description": "원하는 경우, 폐렴 또는 다 른 증상코드를 부가적으로 사용한다.",
                "relevance_score": 0.2
            },
            {
                "code": "R06.8",
                "description": "무호흡 NOS",
                "relevance_score": 0.3
            },
            {
                "code": "R06.2",
                "description": "효천(哮喘)",
                "relevance_score": 0.5
            }
        ]
    },
    {
        "code": "J34.2",
        "description": "Deviated nasal septum",
        "subCodes": [
            {
                "code": "J34.2",
                "description": "편위된 비중격\r\n Deviated nasal septum",
                "relevance_score": 0.6
            },
            {
                "code": "J34",
                "description": "비중격의 정맥류궤양(I86.8)",
                "relevance_score": 0.3
            },
            {
                "code": "J34.1",
                "description": "코 및 비동의 낭 및 점액류",
                "relevance_score": 0.3
            },
            {
                "code": "J34.8",
                "description": "비중격의  천공 NOS\r\n Deviated nasal septum",
                "relevance_score": 0.3
            },
            {
                "code": "Q30",
                "description": "비중격의 선천편위(Q67.4)",
                "relevance_score": 0.3
            },
            {
                "code": "Q30.2",
                "description": "열창, 파임 및 갈림 코",
                "relevance_score": 0.3
            },
            {
                "code": "Q67.4",
                "description": "선천성 비중격의 편위",
                "relevance_score": 0.4
            },
            {
                "code": "M95.0",
                "description": "편위된 비중격(J34.2)",
                "relevance_score": 0.6
            }
        ]
    },
    {
        "code": "R42",
        "description": "Dizziness and giddiness",
        "subCodes": [
            {
                "code": "R42",
                "description": "어지럼증 및 어지럼\r\n Dizziness and giddiness",
                "relevance_score": 0.6
            },
            {
                "code": "D13.2",
                "description": "십이지장의 양성 신생물",
                "relevance_score": 0
            },
            {
                "code": "D03",
                "description": "행동양식분류코드 /2의 형태분류코드 M872-M879",
                "relevance_score": 0.1
            },
            {
                "code": "D21",
                "description": "연골의 기타 양성 신생물",
                "relevance_score": 0.1
            },
            {
                "code": "U07.0",
                "description": "원하는 경우, 폐렴 또는 다른 증상코드를 부가적으로 사용한다.",
                "relevance_score": 0.1
            },
            {
                "code": "R27.8",
                "description": "기타 및 상세불명의 협조결여",
                "relevance_score": 0.3
            },
            {
                "code": "R27",
                "description": "현기증 NOS(R42)",
                "relevance_score": 0.5
            },
            {
                "code": "R29.6",
                "description": "어지럼증 및 어지럼(R42)",
                "relevance_score": 0.7
            }
        ]
    },
    {
        "code": "R53",
        "description": "Malaise and fatigue",
        "subCodes": [
            {
                "code": "R53",
                "description": "병감 및 피로\r\n Malaise and fatigue",
                "relevance_score": 0.7
            },
            {
                "code": "F48.0",
                "description": "병감 및 피로(R53)",
                "relevance_score": 0.7
            }
        ]
    }
]
'''