import {request} from "../utils/requests";


export function getNotifies() {
    return request.request({
        url: '/notify/',
        method: 'get',
    })
}


export function modifyNotify(data: any) {
    data.payload = JSON.stringify(data.payload)
    return request.request({
        url: '/notify/',
        method: data.id ? "put" : "post",
        data: data
    })
}
