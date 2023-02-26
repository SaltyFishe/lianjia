<template>
  <div class="app-container">
    <el-form ref="form" :rules="rules" :model="form" label-width="150px" style="width: 600px">
      <el-form-item label="手机号：" prop="phone">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="昵称：" prop="userName">
        <el-input v-model="form.userName" />
      </el-form-item>
      <el-form-item label="生日：" prop="birthday">
        <el-input v-model="form.birthday" />
      </el-form-item>
      <el-form-item label="性别：" prop="sex">
        <el-input v-model="form.sex" />
      </el-form-item>
      <el-form-item label="城市：" prop="city">
        <el-input v-model="form.city" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handModify">确认修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getInfo } from '@/api/user'

export default {
  data() {
    const validateSex = (rule, value, callback) => {
      if (!['男', '女'].includes(value)) {
        callback(new Error('性能只能为男或女'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('长度不能小于6位'))
      } else {
        callback()
      }
    }
    return {
      form: {
        phone: '',
        password: '',
        newPassword: '',
        newPassword2: '',
        userName: '',
        birthday: '',
        sex: '',
        city: ''
      },
      rules: {
        phone: [{ required: true, message: '请输入手机号码', trigger: 'blur' }],
        userName: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        password2: [{ required: true, trigger: 'blur', validator: validatePassword }],
        city: [{ required: true, message: '请输入所在城市', trigger: 'blur' }],
        sex: [{ required: true, validator: validateSex, trigger: 'blur' }],
        birthday: [{ required: true, message: '请输入生日日期', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    this.info()
  },
  methods: {
    info() {
      getInfo().then(response => {
        this.form.phone = response.data.name
        this.form.city = response.data.city
        this.form.sex = response.data.sex
        this.form.birthday = response.data.birthday
        this.form.userName = response.data.user_name
      })
    },
    onSubmit() {
      this.$message('submit!')
    },
    handModify() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/modify', this.form).then(() => {
            this.$message.success('修改更新成功！')
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

