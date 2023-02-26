<template>
  <div class="dashboard-container">
    <div class="dashboard-text">您好，{{ name }}！ 欢迎使用链家分析系统 </div>
    <template>
      以下为最新采集的二手房产信息：
      <el-carousel :interval="5000" type="card" height="600px" >
        <el-carousel-item v-for="item in data" :key="item">
          <div style="display: flex">
            <el-image :src="item.image_url" :fit="fit"></el-image>
            <el-card style="min-width: 200px">
              <el-link :href="item.url" style="margin-bottom: 5px;" target="_blank"><el-header>{{ item.title }}</el-header></el-link><br>
              面积:<span style="margin: 10px">{{ item.size }}</span>平方米<br>
              卖价:<span style="margin: 10px">{{ item.price }}</span>万元<br>
              装修:<span style="margin: 10px">{{ item.decorate }}</span><br>
            </el-card>
          </div>
        </el-carousel-item>  //走马灯
      </el-carousel>
    </template>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getLast } from '@/api/table'

export default {
  name: 'Dashboard',
  data() {
    return {
      data: [],
      fit: 'contain'
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  mounted() {
    this.getDashboardPics()
  },
  methods: {
    getDashboardPics() {
      getLast().then(response => {
        this.data = response.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
    text-align: center;
    margin-bottom: 30px;
  }
}
.el-carousel__item h3 {
  color: #f1f2f5;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #fafbfd;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: white;
}
</style>
