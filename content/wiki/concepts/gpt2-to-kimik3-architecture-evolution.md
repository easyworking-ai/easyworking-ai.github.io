---
title: "GPT-2에서 KimiK3까지: 7년간 LLM 구조가 진화한 방식"
description: "GPT-2(2019)에서 KimiK3(2026)까지, LLM 아키텍처가 7단계에 걸쳐 어떻게 바뀌었는지를 비유와 코드로 정리한 심층 가이드. Linear Attention, DeltaNet, Gated DeltaNet, KDA, MoE, AttnRes까지."
created: 2026-07-29
updated: 2026-07-29
cssclass: wiki-concept
section: CONCEPTS
publish: true
lang: ko
tags:
  - llm
  - architecture
  - linear-attention
  - transformer
  - model-design
cover:
audio:
---

## 기억을 버리는 법을 배운 AI

2026년, 성능이 가장 좋은 언어모델은 더 많이 기억하지 않는다. 오히려 더 효율적으로 잊는다.

이 역설이 LLM 아키텍처 7년의 진화를 한 문장으로 요약한다. 2019년 GPT-2는 1억 2,400만 개의 매개변수로 문맥 안의 모든 단어를 펼쳐놓고 동시에 읽었다. 2026년 KimiK3는 2조 8,000억 개의 매개변수로 정해진 공간 안에서 무엇을 버리고 무엇을 남길지 선택한다. 7년 사이 모델 크기는 22,580배 커졌지만, 진짜 변화는 크기가 아니라 구조에 있다.

왜 구조를 바꿔야 했나. GPT-2의 attention에는 설계상의 한계가 있었다. 문장의 모든 단어 쌍을 비교하므로, 문맥이 길어지면 연산량이 제곱으로 늘어나고 메모리는 선형으로 쌓인다. 10만 토큰을 처리하려면 모델의 96개 층마다 10만 개의 Key-Value 벡터를 보관해야 한다. 문맥이 늘어날수록 기억의 비용이 감당하기 어려워진다.

이 벽을 넘기 위해 7년간 일곱 번의 설계 전환이 일어났다. 각 전환은 같은 질문에 대해 다른 대답을 내놓았다:

> **고정된 공간에 정보를 저장할 때, 무엇을 기억하고 무엇을 잊을 것인가?**

Linear Attention은 요약 노트에 압축했다. DeltaNet은 같은 자리에 있으면 지우고 다시 썼다. KDA는 정보 종류마다 다르게 잊었다. KimiK3는 이 대답들을 한 건물 안에 섞어놓았다. 이 글은 그 대답들이 어떻게 이어지는지를 따라간다.

![GPT-2에서 KimiK3까지 7단계 진화 타임라인](/static/images/gpt2-kimik3/2026-07-28-gpt2-kimik3-timeline-infographic.png)

| 단계 | 연도 | 핵심 질문 | 비유 |
|---|---|---|---|
| GPT-2 | 2019 | 기본 attention은 어떻게 작동하는가? | 모든 쪽지를 펼쳐놓고 읽기 |
| Linear Attention | 2020 | 쪽지가 너무 많아지면? | 노트 한 권에 요약해 적기 |
| DeltaNet | 2021 | 요약 노트가 꽉 차면? | 노트를 지우고 다시 쓰기 |
| DeltaNet 병렬화 | 2024 | 지우고 쓰는 걸 빠르게 하려면? | 묶음으로 처리하기 |
| Gated DeltaNet | 2025 | 노트를 전체적으로 비우고 싶으면? | 시간이 지나면 흐려지는 잉크 |
| KDA / Kimi Linear | 2025 | 채널마다 다르게 잊고 싶으면? | 색깔별로 다른 지움판 |
| KimiK3 | 2026 | 이걸 2.8조 매개변수로 키우면? | 여러 층 건물 + 전문가 부서 + 비서 |

### 원문 참고 이미지

![GPT-2부터 KimiK3까지의 구조 진화를 다룬 원문 참고 이미지](/static/images/gpt2-kimik3/2026-07-29-gpt2-kimik3-waterloo-reference.jpg)

*원문 아티클([From GPT2 to Kimi3, Explained](https://x.com/waterloo_intern/status/2081762065392541951), ali @waterloo\_intern)을 바탕으로 학습 순서를 잡을 때 참고한 이미지.*

---

## 1. GPT-2: 모든 쪽지를 펼쳐놓고 읽기 (2019)

GPT-2의 attention을 독서실에 비유해보자. 문장의 모든 단어를 번호표(임베딩)로 바꾸고, 각 단어가 몇 번째 자리에 있는지 표시한 뒤, 12단계의 독해 과정을 거친다. 이 과정에서 "이 단어랑 저 단어가 연결되어 있구나"를 파악하는 게 attention이다.

Attention의 핵심은 Q(Query), K(Key), V(Value) 세 가지 벡터다. 각 토큰이 "내가 찾는 정보가 이거다"(Q)라고 묻고, 다른 토큰들이 "나는 이런 정보를 가지고 있다"(K)라고 답하며, 매칭이 된 토큰의 실제 내용(V)을 가져온다.

```python
# GPT-2의 attention 핵심 — softmax 정규화로 가중치 계산
scores = Q @ K.transpose(-1, -2) / math.sqrt(d_head)
attn = softmax(scores, dim=-1)
out = attn @ V
```

softmax는 모든 토큰의 가중치를 0~1 사이로 정규화하면서 합이 1이 되게 만든다. 이 과정에서 각 토큰은 다른 모든 토큰에 대해 가중치를 계산해야 한다.

### KV Cache와 비용 문제

추론 시 GPT-2는 이전에 계산한 Key, Value를 캐시(KV Cache)에 보관한다. 새 토큰을 생성할 때마다 이전 모든 토큰의 KV를 다시 계산할 필요가 없다.

하지만 캐시 크기는 문맥 길이에 비례해서 커진다. **O(N) 크기의 캐시가 층마다 필요하다.** 문맥이 10만 토큰이면, 모델의 모든 층(96개)에 10만 개의 KV 벡터가 쌓인다. 이것이 GPT-2 이후 모든 아키텍처가 해결하려 한 근본 문제다.

---

## 2. Linear Attention: 쪽지를 노트에 요약하기 (2020)

소프트맥스를 빼면 수학이 단순해진다. Katharopoulos 등이 제안한 [Linear Attention](https://arxiv.org/abs/2006.16236)은 softmax를 ELU+1이라는 단순한 함수로 교체한다.

핵심 통찰은 수식의 결합 법칙이다. 일반 attention은 `(Q × K^T) × V` 순서로 계산한다 — 먼저 N×N 크기의 attention 행렬을 만든다. 하지만 softmax가 없으면 `Q × (K^T × V)` 순서로 바꿀 수 있다. `K^T × V`는 D×D 크기의 고정된 행렬이 된다.

```python
# Linear Attention의 핵심 — D×D 고정 상태에 모든 정보를 압축
q = F.elu(q) + 1   # softmax 대신 ELU+1
k = F.elu(k) + 1
S = k.transpose(-1, -2) @ v   # D×D 상태 (문맥 길이와 무관)
out = q @ S                    # 고정된 상태에서 읽기
```

**요약 노트(D×D)에 모든 쪽지를 요약해 적는 것**과 같다. 노트 크기는 문맥이 길어져도 변하지 않는다. 시간당 비용이 O(N²)에서 O(N)으로 줄어든다.

### 트레이드오프

정확도가 약간 떨어진다. 요약 노트는 원본 쪽지 전체를 펼쳐놓고 읽는 것보다 정보 손실이 크다. D×D 공간에 너무 많은 정보를 우겨넣으면 서로 간섭을 일으킨다. 이 간섭 문제가 다음 진화의 출발점이다.

---

## 3. DeltaNet: 지우고 다시 쓰기 (2021)

요약 노트에 계속 추가만 하면 어떻게 될까. 글씨가 겹쳐서 읽을 수 없게 된다.

Schlag 등의 [Fast Weight Programmers](https://arxiv.org/abs/2102.11174) 연구는 이렇게 말한다: "저장 용량을 초과하면, 모델은 어떤 정보를 지우고 어떤 정보를 남길지 선택할 수 있어야 한다."

DeltaNet의 해법은 **새 정보를 쓰기 전에, 같은 자리에 있는 옛날 정보를 먼저 지우는 것**이다. 이것을 Delta Rule이라고 부른다.

```python
# Delta Rule의 핵심 — 빼고 더하기
v_old = k @ S                    # ① 현재 키 위치에 뭐가 있는지 읽기
u = beta * (v - v_old)           # ② 차이만 계산 (델타)
S = S + k.transpose(-1, -2) @ u  # ③ 차이만 쓰기 (기존 것은 자동으로 교체됨)
```

화이트보드에 "고양이 = 회색"이라고 적혀 있다. "고양이 = 검은색"으로 바꾸려면:
1. 먼저 보드에서 "고양이 = ?"을 읽는다 → "회색"
2. 새 정보(검은색)에서 옛날 정보(회색)를 뺀다 → 변화분
3. 변화분만 보드에 적는다 → 자동으로 "회색"이 "검은색"으로 교체됨

![메모리 상태 진화: Linear Attention → DeltaNet → Gated DeltaNet → KDA](/static/images/gpt2-kimik3/2026-07-28-memory-evolution-infographic.png)

정밀한 정보 교체가 가능해진 대신, 한 가지 문제가 생긴다. Delta rule은 토큰 하나씩 순차적으로 처리해야 한다. 매 토큰마다 이전 상태 S가 필요하므로 GPU 병렬 처리가 불가능하다. 느리다.

---

## 4. DeltaNet 병렬화: 묶음으로 처리하기 (2024)

순차 처리의 느림을 해결하기 위해 **여러 토큰을 묶음(chunk)으로 처리**하는 방식이 등장했다. 핵심 발상은 단순하다. 묶음 안에서는 일반 attention을 쓰고, 묶음 사이는 요약 노트 방식을 쓴다.

```python
# 청크 크기 C로 분할
for i in range(t // C):
    q_c = q[:, :, i*C:(i+1)*C]   # C개 토큰 묶음
    k_c = k[:, :, i*C:(i+1)*C]
    v_c = v[:, :, i*C:(i+1)*C]

    o_prev = q_c @ S                           # ① 이전 상태에서 읽기 (재귀적)
    attn = (q_c @ k_c.transpose(-1,-2)).tril()  # ② 청크 내 attention
    o_curr = attn @ v_c
    o = o_prev + o_curr                         # 둘을 합침

    S = S + k_c.transpose(-1,-2) @ v_c          # ③ 상태 갱신
```

청크 크기 C가 N이면 일반 attention(O(N²))이 되고, C가 1이면 순수 linear attention(최소 연산량)이 된다. C = 64~128이 GPU 텐서코어에 최적화된 실용적 중간값이다.

Delta Rule을 병렬화하려면 추가적인 수학적 변환이 필요하다. Householder 전이 행렬을 사용해 한 청크의 모든 delta를 한 번에 계산하는 방식이다. 원문 저자가 "이 섹션을 이해하는 데 약 7시간이 걸렸다"고 고백할 정도로, 전체 진화에서 가장 기술적으로 어려운 부분이다.

---

## 5. Gated DeltaNet: 흐려지는 잉크 (2025)

Delta Rule은 "정확한 위치의 정보를 교체"할 수 있다. 하지만 문맥이 전환될 때(display ↔ search 등) 여러 정보를 한꺼번에 지워야 할 수 있다. Delta Rule은 교체할 특정 정보가 있을 때만 지울 수 있다.

Mamba-2에서 가져온 해결책은 간단하다. **시간이 지나면 모든 정보가 조금씩 흐려지게 한다.** 게이트(gate)라는 매개변수를 추가한다.

```python
# Mamba의 단순 게이팅
cache = alpha * S_old + S_new    # alpha로 이전 정보 감쇄
```

- alpha = 1: 순수 linear attention (덧셈만, 감쇄 없음)
- alpha = 0: 메모리 완전 삭제
- 0 < alpha < 1: 점진적 감쇄

| 방식 | 정밀 교체 | 전체 감쇄 |
|---|---|---|
| Delta Rule만 | 가능 | 불가 |
| Mamba Gate만 | 불가 | 가능 |
| **Gated DeltaNet** | **가능** | **가능** |

Gated DeltaNet은 Delta Rule의 정밀 교체와 Mamba의 전체 감쇄를 결합한다. 시간 스텝 x에 쓰인 정보가 시간 스텝 x+t에 읽힐 때, 그 정보는 매 시점의 게이트 값이 누적해서 곱해진 만큼 감쇄된다.

---

## 6. KDA: 색깔별로 다른 지움판 (2025)

Gated DeltaNet의 alpha는 하나의 스칼라 값이다. "전체를 0.7만큼 흐리게 해라" 같은 식으로 작동한다. 하지만 정보의 종류가 여러 가지라면? 인물 정보는 오래 기억하고, 날씨 정보는 빨리 잊고 싶을 수 있다.

**KDA(Kimi Delta Attention)**의 혁신은 채널(정보의 차원)마다 서로 다른 alpha를 학습하는 것이다.

```python
# Gated DeltaNet: alpha는 하나의 스칼라
alpha = torch.sigmoid(self.w_alpha(x))  # shape: (b, t, 1)

# KDA: alpha는 채널별 (d 차원)
alpha = torch.sigmoid(self.w_alpha(x))  # shape: (b, t, d) ← 각 차원마다 다른 값
```

Kimi Linear는 DeltaNet Transformer 대비 세 가지 구조적 변경을 추가했다:

1. **MLA(Multi-head Latent Attention) 하이브리드**: KDA 층 사이사이에 일반 softmax attention 층을 삽입
2. **MoE(Mixture-of-Experts)**: MLP를 전문가 네트워크 집합으로 교체
3. **alpha projection**: DeltaNet에 채널별 게이팅 용량 추가

핵심 주장은 명확하다. Kimi Linear는 통제된 비교에서 **full attention보다 뛰어난 성능**을 보였으며, decode 처리량은 **최대 6배** 높았다. 이것은 단순한 스케일업이 아니다. 추가된 용량은 특정 수학적 목적(채널별 감쇄 제어)을 가진다.

---

## 7. KimiK3: 2.8조 매개변수의 하이브리드 건물 (2026)

![KimiK3 아키텍처: macrocycle 구조 + MoE + AttnRes](/static/images/gpt2-kimik3/2026-07-28-kimik3-architecture-infographic.png)

KimiK3는 23층짜리 대기업 건물이다. 각 층은 4개의 부서(macrocycle)로 이루어진다:

```
[1개 macrocycle = 4개 층]
 KDA | KDA | KDA | MLA      ← 3개는 요약 노트(KDA), 1개는 원본 검색(MLA)
```

- 23개 macrocycle × 4층 = 92개 층
- 3/4는 KDA(고정 크기 메모리), 1/4는 MLA(전체 softmax 검색)
- 첫 번째 층은 dense FFN, 나머지는 latent MoE

### MoE: 898명의 전문가 중 16명 투입

KimiK3는 898명의 전문가 네트워크를 가지고 있다. 매 토큰마다 16명을 선택한다. 항상 같은 2명은 공통 업무를 하고, 나머지 896명 중에서 업무 성격에 맞는 14명을 뽑는다.

전문가들은 **압축된 latent 공간**에서 작동한다. FLOP은 절반으로 줄면서 처리량은 올라간다. 활성화 함수로 SiTU(SiLU 변형)를 사용해 표현력을 늘렸다. 다만 fused kernel 없이는 기존 경로보다 약 3배 느리다는 트레이드오프가 있다.

### KDA와 MLA의 역할 분담

| 컴포넌트 | 메모리 | 역할 |
|---|---|---|
| KDA (3/4) | 고정 크기 상태 | 효율적 순환 메모리 (빠름) |
| MLA (1/4) | 전체 토큰 softmax 검색 | 정확한 정보 검색 (느리지만 정확) |

KDA는 빠르지만 정보를 일부 버려야 한다. MLA는 정확하지만 비용이 크다. KimiK3는 둘을 3:1 비율로 섞어 효율과 정확도를 동시에 잡는다.

### AttnRes: 12층마다 이전 표현 검색

일반적인 신경망에서는 각 층의 입력이 "원본 + 이전 모든 층의 출력"이다. 모든 층의 기여가 동일한 가중치(1)로 더해진다. 하지만 30번째 층은 5번째 층의 출력이 더 중요할 수도 있다.

**AttnRes(Attention Residual)**는 각 층이 학습된 가중치로 이전 층들의 출력을 선택적으로 가져온다. 12층마다 한 번씩 적용해서 비용을 제어한다. KimiK3의 92층 중 8개 AttnRes 블록이 생성되며, 추론 속도는 약 2% 늘지만 연산 효율은 1.25배 향상된다.

KDA 층은 고정 크기 상태로 정보를 일부 버려야 한다. MLA는 토큰 문맥에서 정보를 검색하고, AttnRes는 깊이 방향의 이전 표현에서 정보를 검색한다. 같은 한계(정보 손실)를 서로 다른 방향에서 보완하는 구조다.

---

## 진화의 핵심 원리

7년간의 진화를 하나의 원리로 압축하면 이렇다:

> **고정 용량의 연상 메모리(associative memory)는 결국 eviction policy가 필요하다.** 순수 덧셈은 용량 초과 시 간섭을 만든다. 학습 가능한 선택(gating, routing, decay)이 필수이고, attention이 가장 효과적인 selective-read 메커니즘이다.

각 단계는 세 가지 질문에 대해 다른 대답을 내놓았다:

```
                    ┌─ 저장: 무엇을 기억하는가?
                    │   └─ Key-Value 연상 (모든 단계 공통)
                    │
  각 아키텍처는 ────┼─ 갱신: 어떻게 메모리를 바꾸는가?
                    │   ├─ 덧셈만 (Linear Attention)
                    │   ├─ 빼고 더하기 (DeltaNet)
                    │   ├─ 감쇄 + 델타 (Gated DeltaNet)
                    │   └─ 채널별 감쇄 + 델타 (KDA)
                    │
                    └─ 검색: 고정 공간에서 어떻게 찾는가?
                        ├─ softmax (GPT-2, MLA)
                        ├─ ELU+1 정규화 (Linear Attention)
                        ├─ 정규화된 query @ state (DeltaNet+)
                        └─ 깊이별 attention (AttnRes)
```

비용과 메모리 관점에서 보면:

| 아키텍처 | 상태 크기 | 시간당 비용 | 정확도 |
|---|---|---|---|
| GPT-2 (softmax) | O(N) per 층 | O(N²) | 기준 |
| Linear Attention | O(D²) per 헤드 | O(N) | 약간 낮음 |
| DeltaNet | O(D²) per 헤드 | O(N) (병렬화 시 O(NC)) | 회복 |
| Gated DeltaNet | O(D²) per 헤드 | O(N) | 회복 + 감쇄 |
| KDA | O(D²) per 헤드 | O(N) + alpha 비용 | full attention 수준 |
| KimiK3 | O(D²) KDA + O(N) MLA | 혼합 | full attention 이상 |

---

## 실습: Linear Attention 직접 구현하기

30줄로 Linear Attention의 핵심을 구현할 수 있다.

```python
import torch
import torch.nn.functional as F

class SimpleLinearAttention(torch.nn.Module):
    def __init__(self, dim, heads=4):
        super().__init__()
        self.heads = heads
        self.dim_head = dim // heads
        self.qkv = torch.nn.Linear(dim, dim * 3)
        self.o = torch.nn.Linear(dim, dim)

    def forward(self, x):
        B, T, D = x.shape
        H, dh = self.heads, self.dim_head

        qkv = self.qkv(x)
        q, k, v = qkv.chunk(3, dim=-1)

        q = q.view(B, T, H, dh).transpose(1, 2)
        k = k.view(B, T, H, dh).transpose(1, 2)
        v = v.view(B, T, H, dh).transpose(1, 2)

        # ELU+1 특성 맵 (softmax 대체)
        q = F.elu(q) + 1
        k = F.elu(k) + 1

        # D×D 상태에 접기
        S = k.transpose(-1, -2) @ v  # B, H, dh, dh
        z = k.sum(dim=2, keepdim=True).transpose(-1, -2)

        # 읽기
        out = q @ S
        denom = q @ z
        out = out / (denom + 1e-6)

        out = out.transpose(1, 2).contiguous().view(B, T, D)
        return self.o(out)

# 테스트
x = torch.randn(1, 10, 64)  # batch=1, seq_len=10, dim=64
attn = SimpleLinearAttention(64, heads=4)
y = attn(x)
print(f"Input: {x.shape} → Output: {y.shape}")
```

Delta Rule이 정보 교체를 어떻게 수행하는지도 간단히 실험할 수 있다:

```python
import torch

D = 4
S = torch.zeros(D, D)

# 첫 번째 정보 쓰기
k1 = torch.randn(1, D)
v1 = torch.randn(1, D)
k1 = k1 / k1.norm()
S = S + k1.T @ v1
print("After write 1:", (k1 @ S).squeeze())

# 같은 key에 다른 value로 델타 업데이트
v2 = torch.randn(1, D)
v_old = k1 @ S
delta = v2 - v_old
S = S + k1.T @ delta
print("After update:", (k1 @ S).squeeze())
print("Target v2:    ", v2.squeeze())
# → 두 값이 같아야 한다
```

---

## 참고 문헌

1. ali (@waterloo\_intern), "From GPT2 to Kimi3, Explained" (2026.07) — https://x.com/waterloo_intern/status/2081762065392541951
2. Angelos Katharopoulos et al., "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention" (2020) — https://arxiv.org/abs/2006.16236
3. Immanuel Schlag et al., "Linear Transformers Are Secretly Fast Weight Programmers" (2021) — https://arxiv.org/abs/2102.11174
4. Songlin Yang et al., "Parallelizing Linear Transformers with the Delta Rule over Sequence Length" (2024) — DeltaNet 병렬화
5. Reinforcement Learning Panopticon, "Gated DeltaNet" (2025) — Mamba-2 게이팅과 Delta Rule 결합
6. Kimi (Moonshot AI), "Kimi K2: Trillion-Scale MoE" 기술 문서 — KDA, MLA, per-channel decay 구조
7. Kimi (Moonshot AI), "KimiK3 Technical Report" (2026.07) — macrocycle, AttnRes, Latent MoE, SiTU 활성화 함수
