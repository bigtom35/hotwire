import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import io

st.set_page_config(layout='wide')

ss = st.session_state

if 'figs' not in ss:
    ss['figs'] = []
    ss['fig_names'] = []


def trapezoid_channel_xy(panel_thickness, x_span, channel_height, channel_angle, y_offset=0, units=10):
    fig, ax = plt.subplots(figsize=(8, 3))
    #Bottom
    x_gap = channel_height / np.tan(np.deg2rad(channel_angle)) if channel_angle !=0 else 0
    x_ru = np.array([x_span, x_gap])
    x = np.cumsum(np.tile(x_ru, (1, units*2)).ravel())
    xb = np.concatenate(([0], x))[:x.shape[0]]
    yb = np.tile([0, 0, channel_height, channel_height], (1, units)).ravel() + y_offset

    # Top
    xt = xb
    yt = panel_thickness * np.ones_like(xt) + y_offset

    top, = ax.plot(xt, yt, 'k-')
    bot, = ax.plot(xb, yb, 'k-')
    ax.fill_between(xt, yt, yb, alpha=0.5, lw=0)
    ax.set_aspect('equal')
    ax.set_xlim([0, 150])
    ax.axis('off')
    title = f'{panel_thickness} mm thick, {x_span} mm steps, {channel_height} mm channel depth, {channel_angle}° angle'
    ax.annotate(title, xy=(0.5, 0.75), xycoords='axes fraction', va='center', ha='center', size='x-small')
    ss['figs'].append(fig)
    ss['fig_names'].append(title)


def delete_fig(i):
    del ss['figs'][i]
    del ss['fig_names'][i]

with st.sidebar:
    thick = st.number_input('**Panel Thickness (mm)**', min_value=14, max_value=60, value=17)
    x_span = st.number_input('**Step Width (mm)**', min_value=0, max_value=60, value=5)
    channel_ht = st.number_input('**Channel Height (mm)**', min_value=0, max_value=thick, value=5)
    channel_angle = st.number_input('**Channel Angle (degrees)**', min_value=0, max_value=120, value=45)
    button_clicked = st.button('Make Design', on_click=trapezoid_channel_xy, args=(thick, x_span, channel_ht, channel_angle))


if len(ss['figs']) > 0:
    for i, (fig, fname) in enumerate(zip(ss['figs'], ss['fig_names'])):
        col_fig, col_b1, col_b2 = st.columns([5, 1, 1])
        with col_fig:
            st.pyplot(fig)
        with col_b1:
            fn = fname + '.png'
            img = io.BytesIO()
            fig.savefig(img, format='png')
            btn = st.download_button(label='Save', data=img, file_name=fn, mime='image/png', key=f'save_{i}')
        with col_b2:
            delete_button = st.button('Delete', on_click=delete_fig, args=(i,), key=f'delete_{i}')




