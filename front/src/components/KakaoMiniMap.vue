<script setup>
import { onMounted, ref } from 'vue'
import { loadKakaoMaps } from '../composables/useKakaoMap'

const props = defineProps({
  spots: { type: Array, required: true }, // [{ name, lat, lng }]
})

const mapEl = ref(null)
const failed = ref(false)

onMounted(async () => {
  try {
    const maps = await loadKakaoMaps()
    const center = new maps.LatLng(props.spots[0].lat, props.spots[0].lng)
    const map = new maps.Map(mapEl.value, {
      center,
      level: 5,
      draggable: false,
      scrollwheel: false,
      disableDoubleClick: true,
      disableDoubleClickZoom: true,
    })

    const bounds = new maps.LatLngBounds()
    const path = []
    props.spots.forEach((spot) => {
      const pos = new maps.LatLng(spot.lat, spot.lng)
      bounds.extend(pos)
      path.push(pos)
      new maps.Marker({ map, position: pos, title: spot.name })
    })

    new maps.Polyline({
      map,
      path,
      strokeWeight: 3,
      strokeColor: '#F04E6B',
      strokeOpacity: 0.85,
      strokeStyle: 'shortdash',
    })

    map.setBounds(bounds, 24, 24, 24, 24)
  } catch {
    failed.value = true
  }
})
</script>

<template>
  <div class="minimap">
    <div v-if="!failed" ref="mapEl" class="map"></div>
    <div v-else class="fallback">
      <span>🗺️</span>
      <p>지도를 불러올 수 없어요<br />(Kakao JS 키를 확인해 주세요)</p>
    </div>
    <div class="badge">코스 {{ spots.length }}곳</div>
    <div class="credit"><span class="diamond">◆</span>kakao map</div>
  </div>
</template>

<style scoped>
.minimap {
  position: relative;
  height: 120px;
  background: linear-gradient(135deg, #ebf3ec, #dceaf0);
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
}

.fallback {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 22px;
}

.fallback p {
  font-size: 10px;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.4;
}

.badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(240, 78, 107, 0.92);
  color: #fff;
  border-radius: 8px;
  padding: 3px 8px;
  font-size: 10px;
  font-weight: 700;
  z-index: 2;
}

.credit {
  position: absolute;
  bottom: 6px;
  right: 8px;
  background: rgba(255, 255, 255, 0.88);
  border-radius: 6px;
  padding: 2px 7px;
  font-size: 9px;
  font-weight: 700;
  color: var(--text-sub);
  display: flex;
  align-items: center;
  gap: 3px;
  z-index: 2;
}

.diamond {
  color: #f7c948;
}
</style>
