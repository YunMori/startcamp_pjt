import axios from 'axios'

// FastAPI 백엔드 연동용 axios 인스턴스.
// 백엔드가 준비되면 각 서비스 파일의 USE_MOCK을 false로 바꿔 사용한다.
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000, // Gemini 스토리 생성이 10초를 넘을 수 있어 여유 확보
})

export default http
