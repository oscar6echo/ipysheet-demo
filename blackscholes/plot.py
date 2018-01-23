
import numpy as np
import pandas as pd

import ezhc as hc
import ezvis3d as v3d


def get_html_plot_2d(df_2d):
    """
    """
    label_z = df_2d.columns[0]
    label_x = df_2d.index.name

    g = hc.Highcharts()
    g.chart.width = 790
    g.chart.height = 490
    g.chart.marginLeft = 80
    g.chart.marginTop = 10
    g.chart.marginBottom = 50
    g.chart.alignTicks = False
    g.chart.animation = False
    g.chart.borderColor = '#cccccc'
    g.chart.borderRadius = 0
    g.chart.borderWidth = 1
    g.chart.zoomType = 'xy'

    g.title.text = '{} vs. {}'.format(label_z, label_x)
    g.subtitle.text = ''

    g.xAxis.title.text = label_x
    g.yAxis.title.text = label_z
    g.xAxis.gridLineWidth = 1.0
    g.xAxis.gridLineDashStyle = 'Dot'
    g.yAxis.gridLineWidth = 1.0
    g.yAxis.gridLineDashStyle = 'Dot'

    g.plotOptions.line.marker.enabled = False
    g.plotOptions.line.events.legendItemClick = 'function(){ return false; }'

    g.legend.enabled = False
    g.legend.layout = 'horizontal'
    g.legend.align = 'center'
    g.legend.verticalAlign = 'bottom'
    g.legend.floating = True
    g.legend.maxHeight = 0
    g.legend.x = 0
    g.legend.y = 0
    g.legend.backgroundColor = '#FFFFFF'

    g.tooltip.enabled = True
    g.tooltip.valueDecimals = 4
    g.tooltip.formatter = "function(){ return 'x: <b>'+ this.x.toFixed(4) + '</b>, ' + this.series.name + ': <b>'+ this.y.toFixed(4) +'</b>';}"

    g.credits.enabled = False
    g.exporting.enabled = False

    g.series = hc.build.series(df_2d)

    html = g.html()
    return html


def get_html_plot_3d(df_3d):
    """
    """
    name_x, name_y, name_z = df_3d.columns

    df = df_3d.copy()
    df.columns = ['x', 'y', 'z']

    g = v3d.Vis3d()
    g.width = '790px'
    g.height = '490px'
    g.style = 'surface'
    g.showPerspective = True
    g.showGrid = True
    g.showShadow = False
    g.keepAspectRatio = False
    g.verticalRatio = 0.8
    g.xLabel = name_x
    g.yLabel = name_y
    g.zLabel = name_z
    g.cameraPosition = {'horizontal': 0.9,
                        'vertical': 0.5,
                        'distance': 1.8}

    str_func = """function (point) {
            let x = parseFloat(point.x.toFixed(2));
            let y = parseFloat(point.y.toFixed(2));
            let z = parseFloat(point.z.toFixed(3));
            return '(' + x + ', ' + y + '): ' + '<b> ' + z + '</b > ';
        }"""
    g.tooltip = str_func

    html = g.html(df,
                  center=True,
                  save=False)
    return html
