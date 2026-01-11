/**
 * 图书管理类型定义
 */

/** 图书查询参数 */
export interface BookQuery {
  /** 页码 */
  pageNum: number
  /** 页大小 */
  pageSize: number
  /** 搜索关键词 */
  keywords?: string
  /** 分类 */
  category?: string
  /** 作者 */
  author?: string
}

/** 图书表单对象 */
export interface BookForm {
  /** 图书ID */
  id?: string
  /** 图书标题 */
  title: string
  /** 作者 */
  author: string
  /** ISBN */
  isbn?: string
  /** 出版社 */
  publisher?: string
  /** 出版日期 */
  publishDate?: string
  /** 价格 */
  price: number
  /** 库存数量 */
  stockQuantity: number
  /** 分类 */
  category?: string
  /** 描述 */
  description?: string
  /** 跳转链接 */
  url?: string
  /** 封面图片 */
  cover?: string
}

/** 图书详情对象 */
export interface BookDetail extends BookForm {
  /** 创建时间 */
  createTime: string
  /** 更新时间 */
  updateTime: string
  /** 浏览次数 */
  viewCount: number
}

/** 图书列表项 */
export interface BookItem {
  /** 图书ID */
  id: string
  /** 图书标题 */
  title: string
  /** 作者 */
  author: string
  /** ISBN */
  isbn?: string
  /** 出版社 */
  publisher?: string
  /** 出版日期 */
  publishDate?: string
  /** 价格 */
  price: number
  /** 库存数量 */
  stockQuantity: number
  /** 分类 */
  category?: string
  /** 描述 */
  description?: string
  /** 跳转链接 */
  url?: string
  /** 封面图片 */
  cover?: string
  /** 创建时间 */
  createTime: string
  /** 更新时间 */
  updateTime: string
}