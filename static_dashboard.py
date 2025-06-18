import pickle
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

def add_social_info():
    """Adds social media links to the sidebar with icons"""
    st.sidebar.markdown("""
    <style>
        .social-container {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            padding: 1rem;
            background: rgba(38, 39, 48, 0.2);
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .social-link {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white !important;
            text-decoration: none;
        }
        .social-link:hover {
            opacity: 0.8;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="social-container">
        <h3 style='text-align: center; margin-top: 0;'>Connect With Me</h3>
        <a href="https://www.linkedin.com/in/bennett-preston/" class="social-link" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20">
            LinkedIn
        </a>
        <a href="https://medium.com/@bennett.preston10" class="social-link" target="_blank">
            <img src="https://miro.medium.com/v2/resize:fit:2400/1*sHhtYhaCe2Uc3IU0IgKwIQ.png" width="20">
            Medium
        </a>
        <a href="https://github.com/bspreston10" class="social-link" target="_blank">
            <img src="https://github.githubassets.com/favicons/favicon-dark.png" width="20">
            GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data
def load_spreads(expiration_selector):
    if expiration_selector == '2025-06-27':
        file_path = os.path.join(current_dir, 'data', 'spreads_627.pkl')
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        file_path = os.path.join(current_dir, 'data', 'spreads_1027.pkl')
        with open(file_path, 'rb') as f:
            return pickle.load(f)

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, 'data')
def main():
# ===== SIDEBAR FILTERS =====
    add_social_info()  # Add social media links to the sidebar

    st.sidebar.header("Filters")
    
    metric_selector = st.sidebar.selectbox(
        "Ranking Metric",
        options=['Reward/Risk Ratio', 'Max Loss', 'Max Profit', 
                'Probability of Profit','Score']
    )
    
    top_n_selector = st.sidebar.number_input(
        "Number to Display",
        min_value=1, max_value=100, value=10, step=1
    )
    
    expiration_selector = st.sidebar.selectbox(
        "Select Expiration",
        options=['2025-06-27', '2025-10-17']
    )
    
    # IV and POP filters
    iv_skew_range = st.sidebar.slider("IV Skew", -1.0, 1.0, (-1.0, 1.0), 0.01)
    pop_range = st.sidebar.slider("Probability of Profit", 0.0, 1.0, (0.0, 1.0), 0.05)
    
    st.title("Put Options Credit Spread Analyzer")
    
    # Load data
    try:
        spreads = load_spreads(expiration_selector)
    
        if expiration_selector == '2025-06-27':
            spread_metrics = pd.read_csv(os.path.join(current_dir, 'spreads_metrics_627.csv'))
            scored_spreads = pd.read_csv(os.path.join(current_dir, 'scored_spreads_627.csv'))
            computer_picks = pd.read_csv(os.path.join(current_dir, 'computer_picks_627.csv'))
        else:
            spread_metrics = pd.read_csv(os.path.join(current_dir, 'spreads_metrics_1027.csv'))
            scored_spreads = pd.read_csv(os.path.join(current_dir, 'scored_spreads_1027.csv'))
            computer_picks = pd.read_csv(os.path.join(current_dir, 'computer_picks_1027.csv'))
        
        # Merge metrics with scores
        spread_metrics_total = pd.merge(
            spread_metrics,
            scored_spreads[['long_strike', 'short_strike', 'expiration', 'score']],
            on=['long_strike', 'short_strike', 'expiration'],
            how='left'
        ).copy()
        
        # Add ticker column
        spread_metrics_total['ticker'] = 'NVDA'
        
        # Get computer picks
        computer_picks = computer_picks.rename(columns= {'long_strike': 'Long Strike', 'short_strike': 'Short Strike',
                                                         'current_price': 'Current Price', 'long_ask': 'Long Ask',
                                                         'short_bid': 'Short Bid', 'breakeven': 'Breakeven',
                                                         'net_premium': 'Net Premium', 'probability_of_profit': 'Probability of Profit',
                                                         'reward_risk_ratio': 'Reward/Risk Ratio', 'max_loss': 'Max Loss',
                                                         'max_profit': 'Max Profit', 'score': 'Score', 'iv_skew': 'IV Skew',
                                                         'long_implied_volatility': 'Long IV',
                                                         'short_implied_volatility': 'Short IV',
                                                         'short_black_scholes_price': 'Short BS Price',
                                                         'long_black_scholes_price': 'Long BS Price',
                                                         'short_z_score': 'Short Z-Score',
                                                         'long_z_score': 'Long Z-Score', 'spread_width': 'Spread Width', 'long_open_interest': 'Long Open Interest',
                                                         'short_open_interest': 'Short Open Interest', 'long_delta': 'Long Delta',
                                                         'short_delta': 'Short Delta', 'long_gamma': 'Long Gamma',
                                                         'short_gamma': 'Short Gamma', 'long_theta': 'Long Theta',
                                                         'short_theta': 'Short Theta', 'long_vega': 'Long Vega', 'net_theta': 'Net Theta',
                                                         'short_vega': 'Short Vega', 'long_rho': 'Long Rho',
                                                         'short_rho': 'Short Rho', 'expiration': 'Expiration', 'score': 'Score', 'ticker': 'Ticker'})
        
        
        # ===== MAIN DISPLAY =====
        # Apply filters
        filtered_top = spread_metrics_total[
            (spread_metrics_total['iv_skew'].between(*iv_skew_range)) &
            (spread_metrics_total['probability_of_profit'].between(*pop_range))
        ].copy()
        
        # Rename columns for display
        filtered_top = filtered_top.rename(columns= {'long_strike': 'Long Strike', 'short_strike': 'Short Strike',
                                                         'current_price': 'Current Price', 'long_ask': 'Long Ask',
                                                         'short_bid': 'Short Bid', 'breakeven': 'Breakeven',
                                                         'net_premium': 'Net Premium', 'probability_of_profit': 'Probability of Profit',
                                                         'reward_risk_ratio': 'Reward/Risk Ratio', 'max_loss': 'Max Loss',
                                                         'max_profit': 'Max Profit', 'score': 'Score', 'iv_skew': 'IV Skew',
                                                         'long_implied_volatility': 'Long IV',
                                                         'short_implied_volatility': 'Short IV',
                                                         'short_black_scholes_price': 'Short BS Price',
                                                         'long_black_scholes_price': 'Long BS Price',
                                                         'short_z_score': 'Short Z-Score',
                                                         'long_z_score': 'Long Z-Score', 'spread_width': 'Spread Width', 'long_open_interest': 'Long Open Interest',
                                                         'short_open_interest': 'Short Open Interest', 'long_delta': 'Long Delta',
                                                         'short_delta': 'Short Delta', 'long_gamma': 'Long Gamma',
                                                         'short_gamma': 'Short Gamma', 'long_theta': 'Long Theta',
                                                         'short_theta': 'Short Theta', 'long_vega': 'Long Vega', 'net_theta': 'Net Theta',
                                                         'short_vega': 'Short Vega', 'long_rho': 'Long Rho',
                                                         'short_rho': 'Short Rho', 'expiration': 'Expiration', 'score': 'Score', 'ticker': 'Ticker'})
        
        if not filtered_top.empty:
            # Show metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Avg Net Credit", f"${filtered_top['Net Premium'].mean():.2f}")
            m2.metric("Avg POP", f"{filtered_top['Probability of Profit'].mean():.1%}")
            m3.metric("Best Reward/Risk", f"{filtered_top['Reward/Risk Ratio'].max():.2f}x")
            m4.metric("Top Score", filtered_top['Score'].max())

            n1, n2, n3, n4 = st.columns(4)
            show_top_spreads = n1.checkbox("Show Top Spreads", value=True, key="show_top_spreads")
            show_computer_pick_filter = n2.checkbox("Show Computer Generated Pick", value=True, key="show_computer_picks")
            show_iv = n3.checkbox("Show IV Surface", value=True, key="show_iv_surface")
            show_scatter = n4.checkbox("Show Scatter Plot", value=True, key="show_scatter_plot")
            advanced_metrics = st.selectbox("Show Advanced Options", options=['Yes', 'No'])

            
            # Show top spreads
            if show_top_spreads:
                st.subheader(f"Top {top_n_selector} Spreads")
                
                display_cols = ['Long Strike', 'Short Strike', 'Current Price', 'Probability of Profit',
                            'Reward/Risk Ratio', 'Max Profit', 'Max Loss', 'Score']
                
                
                if advanced_metrics == 'Yes':
                    st.dataframe(filtered_top.nlargest(top_n_selector, metric_selector))
                else:
                    st.dataframe(filtered_top[display_cols].nlargest(top_n_selector, metric_selector))
            else:
                st.warning("Please check the 'Show Top Spreads' option to see the top spreads.")

            
            # Show computer picks
            if show_computer_pick_filter:
                if not computer_picks.empty:
                    st.markdown("### Computer Generated Pick")
                    if advanced_metrics == 'Yes':
                        st.dataframe(computer_picks)
                    else:
                        st.dataframe(computer_picks[['Long Strike', 'Short Strike', 'Current Price', 'Long Ask', 'Short Bid', 
                                                'Breakeven', 'Net Premium', 'Probability of Profit', 
                                                'Reward/Risk Ratio', 'Max Loss', 'Max Profit', 'Score']])
            else:
                st.warning("Please Uncheck the 'Show Computer Picks' option to see computer-generated picks.")
                
            # Show Scatter Plot
            if show_scatter:
                # Let user pick X and Y axes from available numeric columns
                numeric_cols = filtered_top[['Long Strike', 'Short Strike', 'Long Ask',
                                            'Short Bid', 'Net Premium', 'Max Loss', 'Breakeven',
                                            'Probability of Profit', 'Reward/Risk Ratio', 'Max Profit', 'Score',
                                            'Spread Width', 'Long IV', 'Short IV', 'IV Skew',
                                            'Long Open Interest', 'Short Open Interest', 'Net Theta']].columns.tolist()

                # --- Popular Predefined Axis Combos ---
                if show_scatter:
                    popular_combos = {
                        "Reward vs POP": ("Reward/Risk Ratio", "Probability of Profit"),
                        "Max Profit vs Max Loss": ("Max Profit", "Max Loss"),
                        "Net Premium vs POP": ("Net Premium", "Probability of Profit"),
                        "Custom": (None, None)
                    }

                    combo_choice = st.selectbox("Popular Scatterplot Axes", list(popular_combos.keys()))

                    # Initialize defaults
                    default_x, default_y = popular_combos[combo_choice]
                    x_index = numeric_cols.index(default_x) if default_x in numeric_cols else 0
                    y_index = numeric_cols.index(default_y) if default_y in numeric_cols else 1

                    # --- Layout in Columns ---
                    col1, col2 = st.columns(2)
                    with col1:
                        x_axis = st.selectbox("X-axis", options=numeric_cols, index=x_index)
                    with col2:
                        y_axis = st.selectbox("Y-axis", options=numeric_cols, index=y_index)

                    # --- Centered Bubble Size Selector ---
                    st.markdown("### ")
                    st.markdown("<div style='text-align: center'>Bubble Size</div>", unsafe_allow_html=True)
                        
                    size_axis = st.selectbox("", options=numeric_cols, index=numeric_cols.index('score') if 'score' in numeric_cols else 2)

                    # Optional: Show a hint under the selectors
                    st.markdown("<hr>", unsafe_allow_html=True)
                else:
                    return

                filtered_top = filtered_top.nlargest(top_n_selector, metric_selector)

                max_point = filtered_top.loc[filtered_top[size_axis].idxmax()]

                # -- Main scatter plot --
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=filtered_top[x_axis],
                    y=filtered_top[y_axis],
                    mode='markers',
                    marker=dict(
                        size=filtered_top[size_axis],
                        color=filtered_top[size_axis],
                        colorscale='blues',
                        showscale=True,
                        sizemode='area',
                        sizeref=2.*max(filtered_top[size_axis])/(37**2),
                        sizemin=4
                    ),
                    text=filtered_top[['Short Strike', 'Long Strike']].astype(str).agg(' / '.join, axis=1),
                    name=' ',
                    hovertemplate=(
                        f"{x_axis}: %{{x:.3f}}<br>"
                        f"{y_axis}: %{{y:.3f}}<br>"
                        f"{size_axis}: %{{marker.size:.3f}}<br>"
                        "Strikes: %{text}"
                    )
                ))

                # Add a trace for the max bubble
                fig.add_trace(go.Scatter(
                    x=[max_point[x_axis]],
                    y=[max_point[y_axis]],
                    mode='markers',
                    marker=dict(
                        size=[max_point[size_axis]],
                        color='rgba(255, 0, 0, 0)',
                        line=dict(color='red', width=3),
                        sizemode='area',
                        sizeref=2.*max(filtered_top[size_axis])/(37**2),
                        sizemin=4
                    ),
                    name='Max Bubble',
                    hoverinfo='skip'
                ))

                # Title & Layout
                fig.update_layout(
                    title=f"Scatter Plot of {x_axis} and {y_axis} with Max {size_axis} Highlighted",
                    xaxis_title=x_axis,
                    yaxis_title=y_axis,
                    legend=dict(orientation='h', font=dict(size=10))
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please check the 'Show Scatter Plot' option to see the scatter plot.")

            # -- Show IV Surface --
            if show_iv:
                long_options = [spread['long_option'] for spread in spreads]
                short_options = [spread['short_option'] for spread in spreads]

                iv_surface_selector = st.selectbox(
                    "Select IV Surface Type",
                    options=['IV Skew', 'Mid IV', 'Mid Short IV', 'Mid Long IV'],
                    index=0)  # Default to 'IV Skew'

                rows = []

                # Loop through all combinations of long and short options
                for long in long_options:
                    for short in short_options:
                        if (long['bid_iv'] is None or short['ask_iv'] is None or
                            long['bid_iv'] == 0 or short['ask_iv'] == 0):
                            continue

                        row = {
                            'long_implied_volatility_bid': long['bid_iv'],
                            'short_implied_volatility_ask': short['ask_iv'],
                            'short_implied_volatility_ask': short['ask_iv'],
                            'long_implied_volatility_bid': long['bid_iv'],
                            'long_strike': long['strike'],
                            'short_strike': short['strike'],
                            'IV Skew': short['ask_iv'] - long['bid_iv'],
                            'Mid IV': (short['ask_iv'] + long['bid_iv']) / 2,
                            'Mid Short IV': (short['ask_iv'] + short['bid_iv']) / 2,
                            'Mid Long IV': (long['ask_iv'] + long['bid_iv']) / 2
                        }
                        rows.append(row)


                # Build the full DataFrame
                spreads_df = pd.DataFrame(rows)

                # Build the IV surface based on user selection
                if iv_surface_selector == 'IV Skew':
                    value_col = 'IV Skew'
                elif iv_surface_selector == 'Mid Short IV':
                    value_col = 'Mid Short IV'
                elif iv_surface_selector == 'Mid Long IV':
                    value_col = 'Mid Long IV'
                else:
                    value_col = 'Mid IV'

                iv_surface = spreads_df.pivot_table(
                    index='long_strike',
                    columns='short_strike',
                    values=value_col
                ).sort_index(ascending=False)

                # Clean the surface
                iv_surface = iv_surface.replace(0, np.nan).dropna(how='all').dropna(axis=1, how='all')

                # Prepare computer picks
                computer_strikes = computer_picks[['Long Strike', 'Short Strike']].drop_duplicates()
                strike_pairs = list(computer_strikes.itertuples(index=False, name=None))
                show_computer_picks = st.checkbox("Show Computer Pick", value=True)

                # Get z values for those picks
                z_values = []
                for l_strike, s_strike in strike_pairs:
                    try:
                        z_val = iv_surface.loc[l_strike, s_strike]
                    except KeyError:
                        z_val = None
                    z_values.append(z_val)

                
                fig = go.Figure()
                fig.add_trace(go.Surface(
                    z=iv_surface.values,
                    x=iv_surface.columns,
                    y=iv_surface.index,
                    colorscale='Viridis'
                ))
                if show_computer_picks:
                   
                    fig.add_trace(go.Scatter3d(
                        x=[s for (_, s) in strike_pairs],
                        y=[l for (l, _) in strike_pairs],
                        z=z_values,
                        mode='markers+text',
                        marker=dict(size=6, color='red', symbol='x'),
                        text=[f"{l}/{s}" for l, s in strike_pairs],
                        name="Computer Pick"
                    ))

                fig.update_traces(
                    hovertemplate=(
                        f"Short Strike: %{{x}}<br>"
                        f"Long Strike: %{{y}}<br>"
                        f"{value_col}: %{{z:.2f}}<extra></extra>"
                    )
                )
                
                fig.update_layout(
                    width=800,
                    height=900,
                    autosize=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    template='plotly_dark',
                    scene=dict(
                        xaxis_title='Short Strike (Sell)',
                        yaxis_title='Long Strike (Buy)',
                        zaxis_title=value_col,
                        yaxis_autorange='reversed',
                        aspectratio=dict(x=1, y=1, z=0.7),
                        aspectmode='manual'
                    ),
                    updatemenus=[
                        dict(
                            type="buttons",
                            direction="left",
                            buttons=[
                                dict(args=["type", "surface"], label="3D Surface", method="restyle"),
                                dict(args=["type", "heatmap"], label="Heatmap", method="restyle")
                            ],
                            pad={"r": 10, "t": 10},
                            showactive=True,
                            x=0.11,
                            xanchor="left",
                            y=1.1,
                            yanchor="top"
                        )
                    ],
                    annotations=[
                        dict(text='Trace type:', showarrow=False, x=0, y=1.08, yref='paper', align='left')
                    ]
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please check the 'Show IV Surface' option to see the IV surface.")
                
        else:
            st.warning("No spreads match the current filters.")
            
    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")

if __name__ == "__main__":
    main()
