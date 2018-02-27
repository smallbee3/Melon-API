from django import template

register = template.Library()


def ellipsis_line(value, arg):
    # value로부터
    # arg에 주어진 line수만큼의
    # 문자열(Line)을 반환
    # 만약 arg의 line수보다
    #   value의 line이 많으면
    #   마지막에 ...추가

    # 주어진 multi-line string을 리스트로 분할
    lines = value.splitlines()
    # 리스트의 길이가 주어진 arg(line수) 보다 길 경우
    if len(lines) > arg:
        # 줄바꿈 문자 단위로
        # multi-line string을 분할한 리스트를
        #   arg(line수)개수까지 슬라이싱한 결과를 합침
        #   마지막 요소에는 '...'을 추가
        return '\n'.join(lines[:arg] + ['...'])
    # 리스트 길이가 주어진 arg보다 짧으면 원본을 그대로 리턴
    return value


register.filter('ellipsis_line', ellipsis_line)
