using Randomizer.Api.Models;

namespace Randomizer.Api.Extensions
{
    public static class SeedParametersExtensions
    {
        public static string GenerateFilenameScheme(this SeedParameters parameters, string version, long seed)
        {
            return $"IOGR_V{version}_{seed}_{parameters.Difficulty}_{parameters.Goal.Replace(" ", string.Empty)}_{parameters.Mode}_{parameters.Variations}";
        }
    }
}