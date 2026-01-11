import request from '@/utils/request'
import type { BookQuery, BookForm, BookDetail } from '@/types/api/book'

const BASE_URL = '/api/v1/books'

const BookAPI = {
  /**
   * 获取图书列表
   */
  getList(params: BookQuery) {
    return request({
      url: BASE_URL,
      method: 'get',
      params
    })
  },

  /**
   * 获取图书详情
   */
  getById(id: string) {
    return request<BookDetail>({
      url: `${BASE_URL}/${id}`,
      method: 'get'
    })
  },

  /**
   * 新增图书
   */
  create(data: BookForm) {
    return request({
      url: BASE_URL,
      method: 'post',
      data
    })
  },

  /**
   * 更新图书
   */
  update(id: string, data: BookForm) {
    return request({
      url: `${BASE_URL}/${id}`,
      method: 'put',
      data
    })
  },

  /**
   * 删除图书
   */
  deleteById(id: string) {
    return request({
      url: `${BASE_URL}/${id}`,
      method: 'delete'
    })
  }
}

export default BookAPI