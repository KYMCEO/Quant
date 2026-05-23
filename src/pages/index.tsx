import React, { useEffect } from 'react';
import Head from 'next/head';
import CTAButton from '../components/CTAButton'; // 방금 만든 컴포넌트 임포트

// 🚨 [코다리 검증 지점] 페이지가 마운트될 때마다 초기 트래픽 로깅 필수!
const useTracking = () => {
  useEffect(() => {
    console.log(`[ANALYTICS LOG] Page View Detected: LandingPage / Initial Load Time=${new Date().toLocaleTimeString()}`);
    // 실제로는 여기서 사용자 ID, 유입 경로(UTM), 기기 정보 등을 로깅해야 함.
  }, []);
};

const LandingPage: React.FC = () => {
  useTracking(); // 페이지 로드 시 트래킹 실행

  return (
    <>
      <Head>
        {/* 여기에 폰트 및 메타 태그가 들어갈 것입니다 */}
        <title>AI Stock Factory | 규제 격차 해소 솔루션</title>
      </Head>

      <main className="min-h-screen bg-gray-50 pt-20">
        {/* 1. HERO SECTION (규제 위험성 후킹) */}
        <section className="text-center py-20 px-4 max-w-6xl mx-auto">
          <h1 className="text-6xl font-extrabold text-gray-900 mb-4 leading-tight">
            당신의 투자는 안전합니까? 🌐 AI 규제 지뢰밭을 통과하는 법.
          </h1>
          <p className="text-2xl text-yellow-700 mt-6 max-w-3xl mx-auto">
            미국/EU의 데이터 주권 및 전력 인프라 리스크가 당신의 투자 수익률에 미치는 영향을 파악하세요.
          </p>
        </section>

        {/* 2. PROBLEM STATEMENT (문제 인식 강화) */}
        <section className="bg-white py-16 px-4 border-b">
            <div className="max-w-5xl mx-auto text-center">
                <h2 className="text-4xl font-bold mb-8 text-gray-800">
                    [문제 인식] 놓치고 있는 규제 리스크 3가지.
                </h2>
                {/* 여기에 시각화 요소 (Designer가 만든 인포그래픽) 삽입 예정 */}
            </div>
        </section>

        {/* 3. CORE FUNNEL & A/B TEST AREA (결정적 순간) */}
        <section className="py-24 px-4 bg-gray-100">
          <div className="max-w-6xl mx-auto flex justify-around items-start gap-8">

            {/* --- 좌측 CTA: Basic Kit (진단/Low Friction) --- */}
            <div>
                <h2 className='text-3xl font-bold mb-10 text-center'>
                    ✅ 1단계: 리스크 진단으로 시작하기
                </h2>
                <p className="text-lg text-gray-600 mb-8 text-center">
                    가장 먼저, 당신의 포트폴리오가 어떤 규제 위협에 노출되어 있는지 '진단'하는 것부터 시작하세요. (최소 진입 장벽)
                </p>
                <CTAButton 
                    title="AI 주식 포트폴리오 리스크 진단" 
                    subtitle="EU/미국 법규 변화로 인한 잠재적 손실 영역을 분석합니다." 
                    variant="basic" 
                    color="primary" // A 버전: Primary Brand Color
                    onClick={() => console.log("Basic Kit Click - Variant A")} 
                />
            </div>

            {/* --- 우측 CTA: Premium Playbook (완벽한 해결책/High Friction) --- */}
            <div>
                <h2 className='text-3xl font-bold mb-10 text-center'>
                    🚀 2단계: 완벽 실행 매뉴얼 확보하기
                </h2>
                <p className="text-lg text-gray-600 mb-8 text-center">
                    단순 진단을 넘어, 실제로 규제 격차를 역이용하여 수익을 창출하는 '완벽한 행동 매뉴얼'이 필요합니다. (최대 가치 제안)
                </p>
                <CTAButton 
                    title="규제 Gap Playbook 구매" 
                    subtitle="실행 가능한 전술적 지침과 최신 법률 분석을 제공합니다." 
                    variant="premium" 
                    color="bright-orange" // B 버전: Bright Orange #FF6600
                    onClick={() => console.log("Premium Playbook Click - Variant B")} 
                />
            </div>

          </div>
        </section>
      </main>
    </>
  );
};

export default LandingPage;