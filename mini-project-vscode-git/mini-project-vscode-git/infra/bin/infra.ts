// Placeholder TypeScript (infra/bin/infra.ts)
import * as cdk from 'aws-cdk-lib';

export class DemoStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // add constructs here (demo)
  }
}

const app = new cdk.App();
new DemoStack(app, 'surkeyDemoStack', { env: { account: '111111111111', region: 'ca-central-1' } });
app.synth();
