import request from '@/utils/request'

export function getHouseList(params) {
  return request({
    url: '/api/houses',   //源数据接口
    method: 'get',
    params
  })
}

export function searchCar(params) {
  return request({
    url: '/api/houses?age=2',
    method: 'get',
    params
  })
}

export function getLast(params) {
  return request({
    url: '/api/last', //从后端接口拿图片
    method: 'get',
    params
  })
}
