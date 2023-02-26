<template>
  <!--为echarts准备一个具备大小的容器dom-->
  <div style="margin: 10px">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>房子总数(套)</span>
          </div>
          <div class="text item">
            {{ totalHouses }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>精装数量(套)</span>
          </div>
          <div class="text item">
            {{ totalJingZhuangHouses }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>清水数量(套)</span>
          </div>
          <div class="text item">
            {{ totalMaoPeiHouses }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="box-card" shadow="hover">
          <div slot="header" class="clearfix">
            <span>交易总额(万)</span>
          </div>
          <div class="text item">
            {{ totalPrice }}
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <div id="main1" style="height: 400px;" class="grid-content bg-purple"/>
      </el-col>
      <el-col :span="12">
        <div id="main2" style="height: 400px;" class="grid-content bg-purple"/>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <div id="main3" style="height: 400px;" class="grid-content bg-purple"/>
      </el-col>
      <el-col :span="12">
        <div id="main4" style="height: 400px;" class="grid-content bg-purple"/>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24">
        <div id="main6" style="height: 400px;" class="grid-content bg-purple"/>
      </el-col>
    </el-row>
  </div>

</template>
<script>
// eslint-disable-next-line no-unused-vars
import {
  getGeneralData,
  getDecorateData,
  getPriceData,
  getAreaData,
  getSizePriceData,
  getCommunityData
} from '@/api/house'

export default {
  name: '',
  data() {
    return {
      charts: '',
      totalHouses: 0,
      totalPrice: 0,
      totalJingZhuangHouses: 0,
      totalMaoPeiHouses: 0,
      registrationAreas: [],
      registrationAreasHouses: [],
      decorate: [],
      decorateHouses: [],
      priceAreaHouses: [],
      community: [],
      communityHouses: [],
      ageHouses: [],
      cityHouses: [],
      cityCarAge: [],
      cityCarMileage: [],
      cityCarPrice: [],
      sizePrice: [],
      agePrice: [],
      vendors2: [],
      vendorAveragePriceHouses: []
    }
  },
  // 调用
  mounted() {
    this.$nextTick(function () {
      // this.drawPie('main1')
      this.loadGeneralData()
      this.loadRegistrationAreaData()
      this.loadPriceData()
      this.loadCommunityData()
      this.loadDecorateData()
      this.loadSizePriceData()
    })
  },
  methods: {
    async loadGeneralData() {
      const response = await getGeneralData()
      const data = response.data
      this.totalHouses = data.total
      this.totalJingZhuangHouses = data.jingzhuang
      this.totalMaoPeiHouses = data.maopei
      this.totalPrice = data.total_price.price__sum
    },
    async loadRegistrationAreaData() {
      const response = await getAreaData()
      const data = response.data
      for (const d of data) {
        this.registrationAreas.push(d.area)
        this.registrationAreasHouses.push(d.count)
      }
      this.drawRegistrationAreaStatistics('main1')
    },
    async loadPriceData() {
      const response = await getPriceData()
      const data = response.data
      this.priceAreaHouses = data
      this.drawPriceStatistics('main2')
    },
    async loadCommunityData() {
      const response = await getCommunityData()
      const data = response.data
      for (const d of data) {
        this.community.push(d.community)
        this.communityHouses.push(d.count)
      }
      this.drawCommunityStatistics('main3')
    },
    async loadDecorateData() {
      const response = await getDecorateData()
      const data = response.data
      for (const d of data) {
        this.decorate.push(d.decorate)
        this.decorateHouses.push(d.count)
      }
      this.drawDecorateStatistics('main4')
    },
    async loadSizePriceData() {
      const response = await getSizePriceData()
      const data = response.data
      this.sizePrice = data
      this.drawMileagePriceStatistics('main6')
    },
    drawCommunityStatistics(id) {
      this.charts = this.$echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          title: {
            text: '各小区二手房分布',
            subtext: '--',
            left: 'center'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: this.community,
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '二手房数量',
              type: 'bar',
              barWidth: '60%',
              data: this.communityHouses,
              itemStyle: {
                normal: {
                  color: '#10cee0'
                }
              }
            }
          ]
        }
      )
    },
    drawRegistrationAreaStatistics(id) {
      this.charts = this.$echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          title: {
            text: '各区二手房分布',
            subtext: '--',
            left: 'center'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: this.registrationAreas,
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '二手房数量',
              type: 'bar',
              barWidth: '60%',
              data: this.registrationAreasHouses,
              itemStyle: {
                normal: {
                  color: '#3991dc'
                }
              }
            }
          ]
        }
      )
    },
    drawPriceStatistics(id) {
      this.charts = this.$echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          title: {
            text: '价格区间占比',
            subtext: '--',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '二手房数量',
              type: 'pie',
              radius: '50%',
              data: this.priceAreaHouses,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
      )
    },
    drawDecorateStatistics(id) {
      this.charts = this.$echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          title: {
            text: '装修情况统计',
            subtext: '--',
            left: 'center'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: this.decorate,
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '二手房数量',
              type: 'bar',
              barWidth: '60%',
              data: this.decorateHouses,
              itemStyle: {
                normal: {
                  color: '#3991dc'
                }
              }
            }
          ]
        }
      )
    },
    drawMileagePriceStatistics(id) {
      this.charts = this.$echarts.init(document.getElementById(id))
      this.charts.setOption(
        {
          title: {
            text: '二手房大小及价格分布',
          },
          grid: {
            left: '3%',
            right: '7%',
            bottom: '7%',
            containLabel: true
          },
          tooltip: {
            // trigger: 'axis',
            showDelay: 0,
            formatter: function(params) {
              if (params.value.length > 1) {
                return params.seriesName + ' :<br/>' + params.value[0] + '平方米 ' + params.value[1] + '万元 '
              } else {
                return params.seriesName + ' :<br/>' + params.name + ' : ' + params.value + '平方米 '
              }
            },
            axisPointer: {
              show: true,
              type: 'cross',
              lineStyle: {
                type: 'dashed',
                width: 1
              }
            }
          },
          toolbox: {
            feature: {
              dataZoom: {},
              brush: {
                type: ['rect', 'polygon', 'clear']
              }
            }
          },
          brush: {
          },
          legend: {
            data: ['房子大小', '价格'],
            left: 'center',
            bottom: 10
          },
          xAxis: [
            {
              type: 'value',
              scale: true,
              axisLabel: {
                formatter: '{value} 万'
              },
              splitLine: {
                show: false
              }
            }
          ],
          yAxis: [
            {
              type: 'value',
              scale: true,
              axisLabel: {
                formatter: '{value} 平方米'
              },
              splitLine: {
                show: false
              }
            }
          ],
          series: [
            {
              name: '大小-价格',
              type: 'scatter',
              emphasis: {
                focus: 'series'
              },
              data: this.sizePrice,
              markArea: {
                silent: true,
                itemStyle: {
                  color: 'transparent',
                  borderWidth: 1,
                  borderType: 'dashed'
                },
                data: [[{
                  name: '大小及价格',
                  xAxis: 'min',
                  yAxis: 'min'
                }, {
                  xAxis: 'max',
                  yAxis: 'max'
                }]]
              },
              markPoint: {
                data: [
                  {type: 'max', name: 'Max'},
                  {type: 'min', name: 'Min'}
                ]
              },
              markLine: {
                lineStyle: {
                  type: 'solid'
                },
                data: [
                  {type: 'average', name: '平均值'},
                  { xAxis: 160 }
                ]
              }
            }
          ]
        }
      )
    },
  }
}
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  list-style: none;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

</style>
