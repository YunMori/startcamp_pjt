// Kakao Maps SDK 로드 대기 헬퍼.
// index.html에서 autoload=false로 스크립트를 불러오므로, kakao.maps.load()가 끝난 뒤 사용해야 한다.
let loadPromise = null

export function loadKakaoMaps() {
  if (loadPromise) return loadPromise
  loadPromise = new Promise((resolve, reject) => {
    if (!window.kakao || !window.kakao.maps) {
      reject(new Error('Kakao Maps SDK가 로드되지 않았어요. VITE_KAKAO_JS_KEY를 확인해 주세요.'))
      return
    }
    window.kakao.maps.load(() => resolve(window.kakao.maps))
  })
  return loadPromise
}
