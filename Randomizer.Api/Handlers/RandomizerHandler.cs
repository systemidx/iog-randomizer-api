using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using Randomizer.Api.Configuration;
using Randomizer.Api.Models;

namespace Randomizer.Api.Handlers
{
    public class RandomizerHandler
    {
        private readonly RandomizerConfiguration _randomizerConfiguration;

        public RandomizerHandler(RandomizerConfiguration randomizerConfiguration)
        {
            _randomizerConfiguration = randomizerConfiguration;
        }

        public async Task<RandomizerRomCreationDetails> CreateRandomizedRomAsync(long seed, UploadedFileDetails uploadedFileDetails, SeedParameters parameters)
        {
            var version = _randomizerConfiguration.RandomizerVersion;
            var randomizedFilename = $"IOGR_V{version}_{seed}";
            var offset = 0;

            using (var process = new Process())
            {
                var cmd = BuildPythonString(version, seed, offset, uploadedFileDetails.FullPath, randomizedFilename, parameters);
                
                process.StartInfo = new ProcessStartInfo("python")
                {
                    Arguments = $"-c \"{cmd}\"",
                    WorkingDirectory = _randomizerConfiguration.PathToRandomizer,
                    RedirectStandardError = true,
                };

                process.Start();
                process.WaitForExit();

                var err = await process.StandardError.ReadToEndAsync();
                if (err.Length > 0)
                    return new RandomizerRomCreationDetails { Success = false };
            }

            var path = $"{uploadedFileDetails.Directory}\\{randomizedFilename}.sfc";
            return new RandomizerRomCreationDetails { Success = true, RomPath = path};
        }

        private string BuildPythonString(string version, long seed, long offset, string path, string filename, SeedParameters parameters)
        {
            var builder = new StringBuilder();
            var firebird = parameters.Firebird ? "True" : "False";

            builder.Append("import iogr_rom;iogr_rom.generate_rom(");
            builder.Append($"'{version}'");
            builder.Append($",{offset}");
            builder.Append($",{seed}");
            builder.Append($",'{path}'");
            builder.Append($",'{filename}'");
            builder.Append($",'{parameters.Difficulty}'");
            builder.Append($",'{parameters.Goal}'");
            builder.Append($",'{parameters.Mode}'");
            builder.Append($",'4'");
            builder.Append($",'{parameters.Variations}'");
            builder.Append($",{firebird})");

            return builder.ToString();
        }
    }
}