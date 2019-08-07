using System;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Randomizer.Api.Models;

namespace Randomizer.Api.Extensions
{
    public static class HttpRequestExtensions
    {
        public static IFormFile GetRomFileFromRequest(this HttpRequest request)
        {
            return request?.Form?.Files?.FirstOrDefault();
        }

        public static long GetSeedFromRequestOrDefault(this HttpRequest request)
        {
            var generatedSeed = DateTime.UtcNow.Ticks;
            
            if (request?.Form == null)
                return generatedSeed;
            
            if (!request.Form.ContainsKey("seed"))
                return generatedSeed;

            return long.TryParse(request.Form["seed"], out var seed) ? seed : generatedSeed;
        }

        public static SeedParameters GetParametersFromRequestOrDefault(this HttpRequest request)
        {
            var parameters = new SeedParameters();
            if (request?.Form == null)
                return parameters;

            if (request.Form.ContainsKey("difficulty"))
                parameters.Difficulty = request.Form["difficulty"];

            if (request.Form.ContainsKey("goal"))
                parameters.Goal = request.Form["goal"];

            if (request.Form.ContainsKey("variant"))
                parameters.Variations = request.Form["variant"];

            if (request.Form.ContainsKey("mode"))
                parameters.Mode = request.Form["mode"];

            if (request.Form.ContainsKey("firebird") && bool.TryParse(request.Form["firebird"], out var firebird)) 
                parameters.Firebird = firebird;
            else
                parameters.Firebird = false;

            return parameters;
        }
        
        
    }
}
