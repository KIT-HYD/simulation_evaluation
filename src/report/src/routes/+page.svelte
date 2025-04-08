<script>
    import { metrics } from '$lib/report_data.js';
    import { config } from '$lib/config.js';
    import { names } from '$lib/report_data.js';
    import { plots } from '$lib/plot_data.js';

    let selectedName = $state(names[0]); // Default to first name
    let chartElement;

    let currentPlot = $derived(plots[selectedName]);
    //$: console.log(currentPlot)
    //$: console.log(selectedName)

    $effect(() => {
        if (chartElement) {
            Plotly.newPlot(chartElement, currentPlot, {
                responsive: true,
                displayModeBar: false
            });
            // Force Plotly to maintain container size
            window.addEventListener('resize', () => {
                Plotly.Plots.resize(chartElement);
            });
        }
    })
    // $: () => {
    //     const chart = document.getElementById('chart');
    //     if (chart) {
    //         Plotly.newPlot(chart, currentPlot);
    //     }
    // }
    
</script>

<div class="container mx-auto px-4 py-8">
    <!-- Header with Navigation -->
    <header class="bg-white shadow-sm mb-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-4">
                    <h1 class="text-2xl font-semibold text-gray-900">{config.title}</h1>
                    <select 
                        bind:value={selectedName}
                        class="block w-48 rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    >
                        {#each names as name}
                            <option value={name}>{name}</option>
                        {/each}
                    </select>
                </div>
                <nav class="flex space-x-4">
                    <a href="#chart" class="text-gray-600 hover:text-gray-900">Chart</a>
                    <a href="#metrics" class="text-gray-600 hover:text-gray-900">Metrics</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Chart Section -->
    <section id="chart" class="mb-12">
        <h2 class="text-xl font-semibold mb-4">Performance Chart</h2>
        <div bind:this={chartElement} class="w-full h-[450px] bg-gray-200 rounded-lg overflow-hidden"></div>
    </section>

    <!-- Metrics Table -->
    <section id="metrics" class="mb-12">
        <h2 class="text-xl font-semibold mb-4">Performance Metrics</h2>
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Catchment</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">NSE</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">KGE</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">R²</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MSE</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RMSE</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each Object.entries(metrics) as [catchment, metric]}
                        <tr 
                            class="cursor-pointer hover:bg-gray-50 {catchment === selectedName ? 'bg-indigo-50' : ''}"
                            onclick={() => selectedName = catchment}
                        >
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{catchment}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{metric.NSE.toFixed(4)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{metric.KGE.toFixed(4)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{metric['R²'].toFixed(4)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{metric.MSE.toFixed(4)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{metric.RMSE.toFixed(4)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </section>
</div>
