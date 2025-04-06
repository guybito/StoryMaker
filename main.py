from PlotGenieBasic import PlotGenieBasic
from PlotGenie import PlotGenie

pg_basic = PlotGenieBasic()
pg = PlotGenie()

plot = pg.generate_plot(show_theme=True, save=True)
print(pg.describe_plot())
