<template>
  <div class="app-container">
    <div class="header-container">
      <el-button type="primary" @click="handleAdd" icon="Plus">
        新增图书
      </el-button>
      <el-input
        v-model="queryParams.keywords"
        placeholder="请输入图书名称或作者"
        style="width: 300px; margin-left: 20px;"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #suffix>
          <el-icon @click="handleSearch"><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <el-table
      v-loading="loading"
      :data="bookList"
      row-key="id"
      style="width: 100%; margin-top: 20px;"
    >
      <el-table-column type="index" label="序号" width="60" align="center" />
      <el-table-column prop="id" label="ID" width="80" sortable />
      <el-table-column label="封面" width="100">
        <template #default="{ row }">
          <el-image
            style="width: 50px; height: 50px"
            :src="row.cover"
            :preview-src-list="[row.cover]"
            fit="cover"
            preview-teleported
          />
        </template>
      </el-table-column>
      <el-table-column prop="title" label="图书标题" min-width="200" />
      <el-table-column label="链接" min-width="150" show-overflow-tooltip>
        <template #default="{ row }">
          <a :href="row.url" target="_blank" class="text-blue-500 hover:text-blue-700" @click.stop>{{ row.url }}</a>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="作者" width="150" />
      <el-table-column prop="isbn" label="ISBN" width="180" />
      <el-table-column prop="publisher" label="出版社" width="150" />
      <el-table-column prop="publishDate" label="出版日期" width="120" />
      <el-table-column prop="price" label="价格" width="100">
        <template #default="{ row }">
          ¥{{ row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="stockQuantity" label="库存" width="100" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)" link>
            编辑
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(row.id)" link>
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="queryParams.pageNum"
      v-model:page-size="queryParams.pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      background
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      style="margin-top: 20px; justify-content: flex-end;"
    />
  </div>

  <!-- 编辑弹窗 -->
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="600px"
    @close="handleDialogClose"
  >
    <el-form
      ref="bookFormRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
    >
      <el-row>
        <el-col :span="24">
          <el-form-item label="封面" prop="cover">
            <el-upload
              class="avatar-uploader"
              action="/api/v1/files"
              :show-file-list="false"
              :on-success="handleUploadSuccess"
              :before-upload="beforeUpload"
            >
              <img v-if="formData.cover" :src="formData.cover" class="avatar" style="width: 100px; height: 100px; object-fit: cover; border-radius: 6px;" />
              <el-icon v-else class="avatar-uploader-icon" style="border: 1px dashed #d9d9d9; border-radius: 6px; cursor: pointer; position: relative; overflow: hidden; font-size: 28px; color: #8c939d; width: 100px; height: 100px; text-align: center; line-height: 100px;"><Plus /></el-icon>
            </el-upload>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="图书标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入图书标题" />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="链接地址" prop="url">
            <el-input v-model="formData.url" placeholder="请输入跳转链接 (例如: https://...)" />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="作者" prop="author">
            <el-input v-model="formData.author" placeholder="请输入作者" />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="ISBN" prop="isbn">
            <el-input v-model="formData.isbn" placeholder="请输入ISBN" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出版社" prop="publisher">
            <el-input v-model="formData.publisher" placeholder="请输入出版社" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出版日期" prop="publishDate">
            <el-date-picker
              v-model="formData.publishDate"
              type="date"
              placeholder="请选择出版日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="价格" prop="price">
            <el-input-number
              v-model="formData.price"
              :precision="2"
              :step="1"
              style="width: 100%"
              placeholder="请输入价格"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="库存" prop="stockQuantity">
            <el-input-number
              v-model="formData.stockQuantity"
              :step="1"
              style="width: 100%"
              placeholder="请输入库存数量"
            />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="分类" prop="category">
            <el-select
              v-model="formData.category"
              placeholder="请选择分类"
              style="width: 100%"
            >
              <el-option label="文学" value="literature" />
              <el-option label="科技" value="technology" />
              <el-option label="历史" value="history" />
              <el-option label="艺术" value="art" />
              <el-option label="经济" value="economics" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="3"
              placeholder="请输入图书描述"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import BookAPI from '@/api/book'

// 定义响应式数据
const loading = ref<boolean>(true)
const dialogVisible = ref<boolean>(false)
const dialogType = ref<'add' | 'edit'>('add')

// 查询参数
const queryParams = reactive({
  pageNum: 1,
  pageSize: 10,
  keywords: ''
})

// 分页数据
const total = ref<number>(0)
const bookList = ref<any[]>([])

// 表单数据
const formData = ref({
  id: '',
  title: '',
  author: '',
  isbn: '',
  publisher: '',
  publishDate: '',
  price: 0,
  stockQuantity: 0,
  category: '',
  description: '',
  url: '',
  cover: ''
})

// 表单验证规则
const formRules = {
  title: [{ required: true, message: '请输入图书标题', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stockQuantity: [{ required: true, message: '请输入库存', trigger: 'blur' }]
}

// 表单引用
const bookFormRef = ref()

// 获取图书列表
const getList = async () => {
  loading.value = true
  try {
    const response = await BookAPI.getList(queryParams)
    bookList.value = response.list
    total.value = response.total
  } catch (error) {
    console.error('获取图书列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  queryParams.pageNum = 1
  getList()
}

// 重置
const resetQuery = () => {
  queryParams.keywords = ''
  queryParams.pageNum = 1
  getList()
}

// 分页大小变化
const handleSizeChange = (val: number) => {
  queryParams.pageSize = val
  getList()
}

// 当前页变化
const handleCurrentChange = (val: number) => {
  queryParams.pageNum = val
  getList()
}

// 添加图书
const handleAdd = () => {
  dialogType.value = 'add'
  formData.value = {
    id: '',
    title: '',
    author: '',
    isbn: '',
    publisher: '',
    publishDate: '',
    price: 0,
    stockQuantity: 0,
    category: '',
    description: '',
    url: '',
    cover: ''
  }
  dialogVisible.value = true
}

// 编辑图书
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  formData.value = { ...row }
  dialogVisible.value = true
}

// 删除图书
const handleDelete = async (id: string) => {
  try {
    await ElMessageBox.confirm('确认删除该图书吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await BookAPI.deleteById(id)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    console.error('删除图书失败:', error)
  }
}

// 上传成功回调
const handleUploadSuccess = (response: any) => {
  formData.value.cover = response.data.fileUrl
  ElMessage.success('上传成功')
}

// 上传前校验
const beforeUpload = (rawFile: any) => {
  if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await bookFormRef.value.validate()
    
    if (dialogType.value === 'add') {
      await BookAPI.create(formData.value)
      ElMessage.success('新增成功')
    } else {
      await BookAPI.update(formData.value.id, formData.value)
      ElMessage.success('修改成功')
    }
    
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('提交失败:', error)
  }
}

// 关闭对话框
const handleDialogClose = () => {
  bookFormRef.value?.clearValidate()
}

// 页面初始化
onMounted(() => {
  getList()
})

// 计算属性
const dialogTitle = computed(() => {
  return dialogType.value === 'add' ? '新增图书' : '编辑图书'
})
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>