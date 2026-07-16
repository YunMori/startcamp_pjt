// 설문 문항 — ai_chat 추천 알고리즘(user_type_select.py)과 1:1 대응
// key는 백엔드 POST /api/recommend 의 요청 필드명
export const SURVEY = [
  {
    key: 'mobility',
    q: '먼저, 두 분의 이동 수단은 어떻게 되나요?',
    chips: [
      { label: '뚜벅이 🚶', value: 'walk' },
      { label: '자동차 🚗', value: 'car' },
    ],
  },
  {
    key: 'festival',
    q: '요즘 대전·충청 지역에 핫한 축제들이 열리고 있어요! 관심 있으신가요?',
    chips: [
      { label: '네, 가보고 싶어요 🎉', value: true },
      { label: '아니요, 조용히 보낼래요 ☕', value: false },
    ],
  },
  {
    key: 'q1',
    q: '가장 선호하는 데이트 분위기는 무엇인가요?',
    chips: [
      { label: '세련되고 트렌디한 도심 🏙️', value: '1' },
      { label: '고즈넉하고 감성적인 골목길 📸', value: '2' },
      { label: '탁 트인 자연과 여유 🍃', value: '3' },
    ],
  },
  {
    key: 'q2',
    q: '데이트 중 선호하는 활동은 무엇인가요?',
    chips: [
      { label: '액티비티나 체험 💦', value: '1' },
      { label: '풍경·전시 보며 걷기 📷', value: '2' },
      { label: '한 곳에서 오래 딥톡 ☕', value: '3' },
    ],
  },
  {
    key: 'q3',
    q: '오늘의 식사·음주 스타일은 어떤 쪽이에요?',
    chips: [
      { label: '분위기 좋은 식당과 카페 🍽️', value: '1' },
      { label: '왁자지껄 시원한 맥주 한 잔 🍻', value: '2' },
      { label: '가성비 좋은 로컬 노포 🍜', value: '3' },
    ],
  },
  {
    key: 'q4',
    q: '오늘 데이트의 하이라이트 시간대는 언제인가요?',
    chips: [
      { label: '햇살 좋은 낮 ☀️', value: '1' },
      { label: '저녁 노을부터 야경까지 🌙', value: '2' },
      { label: '하루 종일 ⏰', value: '3' },
    ],
  },
  {
    key: 'q5',
    q: '마지막! 데이트로 스트레스를 어떻게 푸시나요?',
    chips: [
      { label: '축제·핫플의 에너지 🎉', value: '1' },
      { label: '둘만의 프라이빗한 휴식 🤫', value: '2' },
      { label: '스포츠·오락으로 승부욕 🔥', value: '3' },
    ],
  },
]

// 추천 코스 5종 (course_A~E) — ai_chat의 코스 정의와 동일, 좌표는 pre_result 실데이터 기준
export const COURSES = [
  {
    id: 'course_A',
    name: '대청호 물길 힐링 코스',
    emoji: '🌊',
    tags: ['#자연', '#힐링', '#드라이브'],
    duration: '하루 종일',
    spots: [
      { name: '대청댐', lat: 36.4744, lng: 127.4815 },
      { name: '장태산자연휴양림', lat: 36.2159, lng: 127.3413 },
      { name: '대청호자연수변공원', lat: 36.3726, lng: 127.4747 },
    ],
    region: {
      kind: '지역',
      name: '대전 근교 대청호·장태산 일대',
      isFestival: false,
      period: '',
      emoji: '⛰️',
      image: 'https://tong.visitkorea.or.kr/cms/resource_photo/65/3403365_image2_1.jpg',
      desc: '대전 외곽의 대청호 물길을 따라 달리는 드라이브 코스예요. 탁 트인 대청댐 전망과 메타세쿼이아 숲이 울창한 장태산자연휴양림, 잔잔한 수변공원 산책까지 — 자동차만 있다면 조용히 자연 속에서 힐링하기 딱 좋은 하루가 완성됩니다.',
    },
  },
  {
    id: 'course_B',
    name: '도룡동 실내 액티비티 코스',
    emoji: '🎢',
    tags: ['#실내', '#액티비티', '#트렌디'],
    duration: '약 5시간',
    spots: [
      { name: '스몹 대전', lat: 36.3751, lng: 127.3821 },
      { name: '대전아쿠아리움', lat: 36.3101, lng: 127.421 },
      { name: '대전엑스포시민광장스케이트장', lat: 36.3659, lng: 127.388 },
    ],
    region: {
      kind: '지역',
      name: '대전 도룡동·엑스포 일대',
      isFestival: false,
      period: '',
      emoji: '🛼',
      image: 'https://tong.visitkorea.or.kr/cms/resource/61/3351161_image2_1.jpg',
      desc: '엑스포과학공원이 있는 도룡동은 대전에서 가장 트렌디한 실내 데이트 스팟이 모여 있는 동네예요. 스몹에서 몸으로 놀고, 아쿠아리움에서 여유롭게 구경하고, 스케이트장에서 마무리하는 활동적인 커플에게 추천!',
    },
  },
  {
    id: 'course_C',
    name: '소제동 레트로 감성 코스',
    emoji: '📷',
    tags: ['#감성', '#골목길', '#가성비'],
    duration: '약 4시간',
    spots: [
      { name: '테미오래', lat: 36.3207, lng: 127.4233 },
      { name: '소제동', lat: 36.3342, lng: 127.4393 },
      { name: '대동하늘공원', lat: 36.3317, lng: 127.4516 },
    ],
    region: {
      kind: '지역',
      name: '대전 원도심 (소제동·테미오래)',
      isFestival: false,
      period: '',
      emoji: '🎞️',
      image: 'https://tong.visitkorea.or.kr/cms/resource/62/3526662_image2_1.jpg',
      desc: '옛 관사촌을 개조한 테미오래와 철도관사촌 소제동 카페거리는 레트로 감성이 가득한 대전 원도심의 보석이에요. 골목을 천천히 걷다가 해질녘 대동하늘공원에 올라 야경으로 마무리하면 인생샷은 보장!',
    },
  },
  {
    id: 'course_D',
    name: '유성 도심 축제 데이트 코스',
    emoji: '🎉',
    tags: ['#축제', '#온천', '#맛집'],
    duration: '약 5시간',
    spots: [
      { name: '유성온천문화축제', lat: 36.3607, lng: 127.3577 },
      { name: '유성온천공원', lat: 36.3553, lng: 127.3437 },
      { name: '촌놈들연탄구이 본점', lat: 36.3576, lng: 127.3449 },
    ],
    region: {
      kind: '축제',
      name: '유성온천문화축제 (유성온천공원 일대)',
      isFestival: true,
      period: '축제 일정은 유성구청 공지 참고',
      emoji: '♨️',
      image: 'https://tong.visitkorea.or.kr/cms/resource/97/4059997_image2_1.jpg',
      desc: '온천으로 유명한 유성 한복판에서 열리는 축제 코스예요. 축제 분위기를 만끽하고 유성온천공원 족욕장에서 피로를 풀다가, 저녁엔 연탄구이에 시원한 한 잔까지 — 왁자지껄한 에너지를 좋아하는 커플에게 딱!',
    },
  },
  {
    id: 'course_E',
    name: '공주 역사 & 야밤 축제 코스',
    emoji: '🏯',
    tags: ['#축제', '#역사', '#야경'],
    duration: '하루 종일',
    spots: [
      { name: '공주 공산성', lat: 36.4629, lng: 127.1268 },
      { name: '공주야밤 맥주축제', lat: 36.4702, lng: 127.1275 },
      { name: '베이커리 밤마을', lat: 36.4646, lng: 127.1229 },
    ],
    region: {
      kind: '축제',
      name: '공주야밤 맥주축제 (공산성 일대)',
      isFestival: true,
      period: '축제 일정은 공주시 공지 참고',
      emoji: '🍺',
      image: 'https://tong.visitkorea.or.kr/cms/resource/09/3520309_image2_1.jpg',
      desc: '유네스코 세계유산 공산성의 성곽길을 낮에 거닐고, 밤에는 금강변 야밤 맥주축제에서 라이브 공연과 함께 시원한 맥주를! 공주 명물 밤으로 만든 베이커리 디저트까지 챙기면 완벽한 드라이브 데이트가 됩니다.',
    },
  },
]

// 목 리뷰 시드 데이터 (백엔드 연동 실패 시 폴백용)
export const SEED_REVIEWS = {
  course_A: [
    { id: 'r1', nickname: '드라이브장인', rating: 5, date: '2026.06.28', text: '대청호 드라이브 코스 진짜 최고예요. 장태산 메타세쿼이아 숲은 사진 무조건 남기세요!', password: '1234' },
  ],
  course_B: [
    { id: 'r2', nickname: '실내파커플', rating: 4, date: '2026.06.11', text: '더운 날 실내 코스로 딱! 스몹에서 체력 다 쓰고 아쿠아리움에서 쉬는 조합 추천해요.', password: '0000' },
  ],
  course_C: [
    { id: 'r3', nickname: '라떼두잔', rating: 5, date: '2026.07.02', text: '소제동 골목 감성 미쳤어요. 필름카메라 들고 가길 잘했다 싶은 곳이 진짜 많아요!', password: '1234' },
  ],
  course_D: [
    { id: 'r4', nickname: '족욕러버', rating: 4, date: '2026.05.20', text: '축제 기간에 갔는데 분위기 좋았어요. 족욕하고 연탄구이 조합이 의외의 꿀조합!', password: '1111' },
  ],
  course_E: [
    { id: 'r5', nickname: '맥주한잔', rating: 5, date: '2026.06.30', text: '공산성 야경 보면서 마시는 맥주 최고... 밤빵도 꼭 사가세요!', password: '1234' },
  ],
}
