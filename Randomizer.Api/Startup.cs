using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Randomizer.Api.Configuration;
using Randomizer.Api.Handlers;

namespace Randomizer.Api
{
    public class Startup
    {
        private readonly IConfiguration _configuration;

        public Startup(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public void ConfigureServices(IServiceCollection services)
        {
            var randomizerConfiguration = new RandomizerConfiguration();
            
            _configuration.GetSection("Randomizer").Bind(randomizerConfiguration);

            services
                .AddTransient<RandomizerConfiguration>(x => randomizerConfiguration)
                .AddTransient<RandomizerHandler>()
                .AddCors(options=> options.AddPolicy("AllowAll", p => 
                    p
                        .AllowAnyOrigin()
                        .AllowAnyHeader()
                        .AllowAnyMethod()
                        .AllowCredentials()
                        .WithExposedHeaders("Content-Disposition")))
                .AddMvc()
                .SetCompatibilityVersion(CompatibilityVersion.Version_2_2);

            services.Configure<IISOptions>(options => options.ForwardClientCertificate = false);
        }

        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app
                .UseDefaultFiles()
                .UseStaticFiles(new StaticFileOptions{ FileProvider = new PhysicalFileProvider(Path.Combine(Directory.GetCurrentDirectory(), "wwwroot/build"))})
                .UseCors()
                .UseMvc();
        }
    }
}
